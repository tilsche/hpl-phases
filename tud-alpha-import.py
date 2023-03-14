#!/usr/bin/env python3
import asyncio
import csv
import logging

import click
import click_completion
import click_log
import metricq

logger = metricq.get_logger()

click_log.basic_config(logger)
logger.setLevel("INFO")
logger.handlers[0].formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)-8s] [%(name)-20s] %(message)s"
)

click_completion.init()


async def get_average_power(client, metrics, begin, end):
    timelines = [
        list(
            await client.history_raw_timeline(
                metric,
                start_time=begin,
                end_time=end,
            )
        )
        for metric in metrics
    ]

    with open(f"tud-alpha-power.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["time", "power"])

        for metric_data in zip(*timelines):
            # Align timestamps for good measure
            timestamps = [
                timevalue.timestamp.datetime.replace(microsecond=0)
                for timevalue in metric_data
            ]
            timestamp = timestamps[0]
            assert all(ts == timestamp for ts in timestamps)

            power = sum(timevalue.value for timevalue in metric_data)
            csv_writer.writerow([timestamp.isoformat(), power])

    metrics_list = "*".join(metrics)
    print(
        f"Dashboard link: https://metricq.zih.tu-dresden.de/webview/#.{begin.posix_ms}*{end.posix_ms}*{metrics_list}"
    )


async def aanalyze(client, begin, end):
    alpha_nodes_power = [f"taurus.taurusi{n}.power" for n in range(8001, 8035)]
    alpha_pdu_raw_power = [
        f"taurus.H0{a}.E{b}.power" for a in range(1, 5) for b in range(1, 5)
    ]
    alpha_pdu_raw_energy = [
        f"taurus.H0{a}.E{b}.energy" for a in range(1, 5) for b in range(1, 5)
    ]
    alpha_pud_energy = ["taurus.alpha.energy"]

    print("## PDU raw power")
    await get_average_power(client, alpha_pdu_raw_power, begin, end)


async def aget_history(server, token):
    client = metricq.HistoryClient(token=token, management_url=server)
    await client.connect()

    print("# full run")
    await aanalyze(
        client,
        metricq.Timestamp.from_iso8601("2021-05-27T16:31:15+02:00"),
        metricq.Timestamp.from_iso8601("2021-05-27T16:40:29+02:00"),
    )

    # print("# core phase")
    # await aanalyze(
    #     client,
    #     metricq.Timestamp.from_iso8601("2021-05-27T16:32:40.767+02:00"),
    #     metricq.Timestamp.from_iso8601("2021-05-27T16:39:33.109+02:00"),
    # )
    await client.stop()


@click.command()
@click.option("--server", default="amqp://localhost/")
@click.option("--token", default="history-py-dummy")
@click_log.simple_verbosity_option(logger)
def get_history(server, token):
    asyncio.run(aget_history(server, token))


if __name__ == "__main__":
    get_history()
