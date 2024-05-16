"""Tests for the monitor module."""

from sms_simulator.monitor import RowData, generate_table


def test_generate_table() -> None:
    """Test the generate_table function."""
    row_data = RowData()
    table = generate_table(row_data)
    assert [col.header for col in table.columns] == [
        "Number of Refreshes",
        "Queue Size",
        "Sent Messages",
        "Failed Messages",
        "Failure Rate",
        "Throughput (msgs/sec)",
        "Average latency (ms)",
    ]
    assert len(table.rows) == 1
