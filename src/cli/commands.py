import click
import logging
from src.services.blockchain import fetch_validators, fetch_and_store_delegators, fetch_governance_proposals
from src.services.database import insert_validator, insert_or_update_governance_proposal
from src.common.utils import load_config


# Setup logger for this module
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@click.command()
@click.argument('chain_name')
def fetch_and_store_validators(chain_name):
    # Load the specific chain configuration
    chain_config = load_config(chain_name)
    if not chain_config:
        logger.error(f"No configuration found for chain: {chain_name}")
        return

    # Fetch validators using the loaded chain configuration
    validators = fetch_validators(chain_config)
    if validators:
        for validator in validators:
            # Insert each validator into the database
            insert_validator(validator)
            # After inserting a validator, fetch and store its delegators
            # Note: Adjust `fetch_and_store_delegators` to accept validator operator address and chain config
            fetch_and_store_delegators(validator['operator_address'], chain_config)
        logger.info(f"Validators and their delegators for {chain_name} fetched and stored successfully.")
    else:
        logger.warning(f"No validators found for {chain_name}.")


@click.command()
@click.argument('chain_name')
def fetch_and_store_governance_proposals(chain_name):
    chain_config = load_config(chain_name)
    if not chain_config:
        logger.error(f"No configuration found for chain: {chain_name}")
        return

    chain_id = chain_config["chain_id"]  # Extract the chain ID from the configuration

    proposals = fetch_governance_proposals(chain_config)
    if proposals:
        for proposal in proposals:
            insert_or_update_governance_proposal(proposal, chain_id)  # Pass chain_id here
        logger.info(f"Governance proposals for {chain_name} fetched and stored successfully.")
    else:
        logger.warning(f"No governance proposals found for {chain_name}.")


cli.add_command(fetch_and_store_validators)
cli.add_command(fetch_and_store_governance_proposals)
