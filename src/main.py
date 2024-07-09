"""Main entry point for aeromancy-demo-housing (an "AeroMain" file).

This script should be run through Aeromancy runners ("pdm go").
"""

import rich_click as click
from aeromancy import aeromancy_click_options
from rich.console import Console

from aeromancy_demo_housing.action_builder import HousingModelActionBuilder

console = Console()


# Define our CLI options.
@click.command()
# We also need to include a list of standard Aeromancy options.
@aeromancy_click_options
# Make sure to include any new options we created as arguments to aeromain.
def aeromain(**aeromancy_options):
    """CLI application for controlling aeromancy-demo-housing."""
    config = {}  # Empty until we add some hyperparameters.
    console.log("Config parameters from CLI:", config)

    # This builds our Action dependency graph given the configuration passed in.
    action_builder = HousingModelActionBuilder(**config)
    # We create a corresponding runner to execute the dependency graph and kick
    # it off.
    action_runner = action_builder.to_runner()
    action_runner.run_actions(**aeromancy_options)


if __name__ == "__main__":
    aeromain()
