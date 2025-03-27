from snowflake import SnowflakeGenerator
import time


def generate_id(
    instance_id: int = 1,
    epoch: int = int(time.mktime((2025, 1, 1, 0, 0, 0, 0, 0, 0))) * 1000,
) -> str:
    """
    Generate a unique ID using Snowflake algorithm with customizable parameters.

    Args:
        instance_id: The instance/machine ID (default: 1)
        epoch: Custom epoch in milliseconds (default: Jan 1, 2023)

    Returns:
        A unique ID string
    """
    gen = SnowflakeGenerator(instance=instance_id, epoch=epoch)
    return str(next(gen))


if __name__ == "__main__":
    print(generate_id())
