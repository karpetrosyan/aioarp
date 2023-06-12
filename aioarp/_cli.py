import typing

import typer
from typing_extensions import Annotated

import aioarp

app = typer.Typer()

# TODO: add tests

@app.command()
def main(
        interface: Annotated[str,
        typer.Argument(help="Network interface which should be used to send the arp packet.")],
        target_ip: Annotated[str,
        typer.Argument(help="Target IP, the IP address for which we are looking for a mac "
                                                      "address.")],
        timeout: Annotated[typing.Optional[int], typer.Argument(help="Timeout for arp request.")] = None
) -> None:  # pragma: no cover
    try:
        try:
            response = aioarp.request(interface=interface,
                                      target_ip=target_ip,
                                      timeout=timeout)
        except PermissionError:
            text = "To send ARP requests, you must run a script with root privileges."
            print(text)
            return
        ans = response.sender_mac
        text = f"The mac address of IP '{target_ip}' is: {ans}"
        print(text)
    except aioarp.NotFoundError:
        text = f"The IP address {target_ip}' did not respond to our ARP request."
        print(text)


if __name__ == "__main__":
    app()