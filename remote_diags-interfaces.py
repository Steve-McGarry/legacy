from dataclasses import dataclass
import datetime
from re import sub
import os
import json
import asyncio
import aiostream
from typing import Any, AsyncGenerator, Callable, List, Tuple, cast
import aiohttp
import dataclasses_json
import websockets
import dotenv
from bs4 import BeautifulSoup
import csv

def read_env(name: str) -> str:
    value = os.getenv(name)
    assert value is not None, f"missing environment var {name}"
    return value

@dataclass
class EdgeResultSection:
    name: str
    columns: List[str]
    # outer list is the row, inner list is columns for that row
    rows: List[List[str]]

@dataclass
class EdgeInterfaceStatusResult:
    edge_name: str | None
    edge_logical_id: str
    timeout_at: datetime.datetime
    result: List[EdgeResultSection]

def snakify(s: str) -> str:
    return "_".join(
        sub(
            "([A-Z][a-z]+)",
            r" \1",
            sub("([A-Z]+)", r" \1", s.replace("-", " ").replace("IPv6", "ipv6")),
        ).split()
    ).lower()

@dataclass
class CommonData:
    vco: str
    token: str
    enterprise_id: int
    session: aiohttp.ClientSession

    def __post_init__(self):
        self.validate()

        self.session.headers.update({"Authorization": f"Token {self.token}"})

    def validate(self):
        if any(
            missing_inputs := [
                v is None for v in [self.vco, self.token, self.enterprise_id]
            ]
        ):
            raise ValueError(f"missing input data: {missing_inputs}")

@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass()
class EnterpriseEdgeListEdge:
    id: int | None
    logical_id: str | None
    name: str | None
    edge_state: str | None
    activation_state: str | None 

async def do_portal(c: CommonData, method: str, params: dict):
    async with c.session.post(
        f"https://{c.vco}/portal/",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        },
    ) as req:
        resp = await req.json()
        if "result" not in resp:
            raise ValueError(json.dumps(resp, indent=2))
        return resp["result"]

async def get_enterprise_edge_list_raw(
    c: CommonData,
    with_params: list[str] | None,
    filters: dict | None,
    next_page: str | None = None,
) -> dict[str, list | dict]:
    params_object: dict[str, Any] = {
        "enterpriseId": c.enterprise_id,
        "limit": 250,
        "sortBy": [{"attribute": "edgeState", "type": "ASC"}],
    }

    if with_params:
        params_object["with"] = with_params

    if filters:
        params_object["filters"] = filters
    else:
        params_object["_filterSpec"] = True

    if next_page:
        params_object["nextPageLink"] = next_page

    return await do_portal(c, "enterprise/getEnterpriseEdges", params_object)

async def get_enterprise_edge_list_full(
    c: CommonData, with_params: list[str] | None, filters: dict | None
) -> AsyncGenerator[EnterpriseEdgeListEdge, None]:
    next_page = None
    more = True

    while more:
        resp = await get_enterprise_edge_list_raw(c, with_params, filters, next_page)

        meta: dict[str, dict] = cast(dict[str, dict], resp.get("metaData", {}))
        more = meta.get("more", False)
        next_page = cast(str | None, meta.get("nextPageLink", None))

        data: list[dict[str, Any]] = cast(list[dict[str, Any]], resp.get("data", []))
        for d in data:
            yield EnterpriseEdgeListEdge.from_dict(d)  # type: ignore

def process_section(title: str, table: Any) -> EdgeResultSection:
    headers = table.find_all("span", class_="vce-result-header-cell")
    headers = [h.text for h in headers]

    rows = []
    data_rows = table.find_all("div", class_="vce-result-data-row")
    for data_row in data_rows:
        spans = data_row.find_all("span", class_="vce-result-data-cell")
        fields = [span.text for span in spans]
        rows.append(fields)

    return EdgeResultSection(title, headers, rows)

def process_response_data(data) -> List[EdgeResultSection]:
    soup = BeautifulSoup(data, "html.parser")
    section_titles = soup.find_all("h3")
    section_titles = [t.text for t in section_titles]
    section_tables = soup.find_all("div", class_="vce-result-tbl")

    sections = [
        process_section(title, table)
        for (title, table) in zip(section_titles, section_tables)
    ]

    return sections

async def get_interface_statuses(
    c: CommonData,
    edge_logical_ids: List[Tuple[str, str]],
    max_active_edges: int = 5,
    timeout_seconds: int = 60,
) -> List[EdgeInterfaceStatusResult]:
    timeout_at = datetime.datetime.now() + datetime.timedelta(minutes=2)
    queued = list(
        [
            EdgeInterfaceStatusResult(name, logical_id, timeout_at, [])
            for (name, logical_id) in edge_logical_ids
        ]
    )
    num_active = 0
    waiting_for_live: dict[str, EdgeInterfaceStatusResult] = dict()
    waiting_for_action: dict[str, EdgeInterfaceStatusResult] = dict()
    finished: dict[str, EdgeInterfaceStatusResult] = dict()

    async with websockets.connect(
        f"wss://{c.vco}/ws/",
        extra_headers={
            "Authorization": f"Token {c.token}",
        },
    ) as ws:
        # wait for noop with token
        token_msg = json.loads(await ws.recv())
        token: str = token_msg["token"]
        total_done = 0

        # main loop for working thru the task set
        while len(queued) > 0 or num_active > 0:
            # print("{}/{} ({}%) done".format(total_done, len(edge_logical_ids), total_done / len(edge_logical_ids)))
            print(
                "{} queued, {} waiting_for_live, {} waiting_for_action, {} done".format(
                    len(queued),
                    len(waiting_for_live),
                    len(waiting_for_action),
                    len(finished),
                )
            )
            # add more active edges if possible
            new_tasks = set()
            while num_active < max_active_edges and len(queued) > 0:
                edge = queued.pop()
                new_tasks.add(
                    ws.send(
                        json.dumps(
                            {
                                "action": "connectToDevice",
                                "data": {"logicalId": edge.edge_logical_id},
                                "token": token,
                            }
                        )
                    )
                )
                edge.timeout_at = datetime.datetime.now() + datetime.timedelta(
                    seconds=timeout_seconds
                )
                waiting_for_live[edge.edge_logical_id] = edge
                num_active += 1
            if len(new_tasks) > 0:
                await asyncio.gather(*new_tasks)

            # what happens on timeout? is exception thrown?
            try:
                m = json.loads(await asyncio.wait_for(ws.recv(), 5))
                # check msg action and logical ID to handle

                action: str | None = m.get("action", None)
                logicalId: str = m.get("data", {}).get("logicalId", "")
                if action == "connected":
                    e = waiting_for_live.get(logicalId, None)
                    if e:
                        del waiting_for_live[logicalId]
                        num_active -= 1

                        await ws.send(
                            json.dumps(
                                {
                                    "action": "runDiagnostics",
                                    "data": {
                                        "logicalId": logicalId,
                                        "test": "INTERFACE_STATUS",
                                    },
                                    "token": token,
                                }
                            )
                        )
                        waiting_for_action[logicalId] = e
                        num_active += 1
                elif action == "runDiagnostics":
                    e = waiting_for_action.get(logicalId, None)
                    if e:
                        del waiting_for_action[logicalId]
                        num_active -= 1

                        output = (
                            m.get("data", {}).get("results", {}).get("output", None)
                        )
                        if output:
                            e.result = process_response_data(output)
                            finished[logicalId] = e
                            total_done += 1
                        else:
                            # some kind of failure? need to capture info
                            pass
                else:
                    print(m)
            except TimeoutError as e:
                print("timed out waiting for recv")

            now = datetime.datetime.now()
            for id, e in waiting_for_live.items():
                if now > e.timeout_at:
                    del waiting_for_live[id]
                    print("edge {} timed out waiting for live mode".format(e.edge_name))
                    num_active -= 1
            for id, e in waiting_for_action.items():
                if now > e.timeout_at:
                    del waiting_for_action[id]
                    print("edge {} timed out waiting for action".format(e.edge_name))
                    num_active -= 1

    return list(finished.values())

async def main(session: aiohttp.ClientSession):
    common = CommonData(
        read_env("VCO"), read_env("VCO_TOKEN"), int(read_env("ENT_ID")), session
    )

    # stream all edges using paginated API, excluding those which are not CONNECTED
    edge_filter: Callable[[EnterpriseEdgeListEdge], bool] = (
        lambda e: e.edge_state == "CONNECTED"
    )
    chunk_stream = (
        aiostream.stream.iterate(get_enterprise_edge_list_full(common, None, None))
        | aiostream.pipe.filter(edge_filter)
        | aiostream.pipe.chunks(250)
    )

    field_names = None
    headers_done = False

    # process the stream of 100-edge batches
    async with chunk_stream.stream() as s:
        async for edge_batch in s:
            try:
                # build input data for get_interface_statuses function
                edges = [
                    (e.name if e.name else "", e.logical_id)
                    for e in edge_batch
                    if e.logical_id
                ]
                # run diagnostics with 15 concurrent requests
                # TBD how high you can go. 15 seems to work on a low-utilization VCO fine.
                statuses = await get_interface_statuses(common, edges, max_active_edges=15)

                # cache the column names that we output to the CSV
                # this is done so that we can consistently output to CSV with the same column order
                if not field_names:
                    field_names = ['edge_name'] + [snakify(s) for s in {col for e in statuses for section in e.result for col in section.columns}]
                with open('ws-interface-output.csv', 'a') as f:
                    w = csv.DictWriter(f, fieldnames=field_names)

                    # output headers to CSV if this is the first time
                    if not headers_done:
                        w.writeheader()
                        headers_done = True

                    for edge in statuses:
                        # get this edge's column names in each table (routed, switched, modem)
                        headers = {col for section in edge.result for col in section.columns}
                        output_rows = []
                        # flatten the data into several rows - requires duplicating edge name
                        for res in edge.result:
                            for row in res.rows:
                                # assume N/A in every field until we fill it
                                output = {h: "N/A" for h in headers}

                                for i, v in enumerate(row):
                                    # look up the column name for this column based on index
                                    # column name is the key in output objects
                                    k = res.columns[i]
                                    output[k] = v

                                final_output = {
                                    "edge_name": edge.edge_name if edge.edge_name else "N/A"
                                }
                                # snakify all of the column names
                                for k, v in output.items():
                                    final_output[snakify(k)] = v

                                output_rows.append(final_output)

                        # output all rows for the edge to CSV
                        w.writerows(output_rows)

            except Exception as e:
                print(e)

async def main_wrapper():
    async with aiohttp.ClientSession() as session:
        await main(session)

if __name__ == "__main__":
    dotenv.load_dotenv(".env", verbose=True, override=True)
    asyncio.run(main_wrapper())
