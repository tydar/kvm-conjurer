import libvirt
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from conjurer.auth import login_required
from conjurer.auth import get_db

bp = Blueprint('domains', __name__, url_prefix="/domains")

"""
Gets a full list of domain objects from qemu:///system hypervisor
Passes those objects to the template
"""
@bp.route('/')
def list_libvirt_domains():
    try:
        conn = libvirt.open('qemu:///system')
    except libvirt.libvirtError:
        return 'Failed to open connection to the hypervisor'

    domainListFilter = libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE

    try:
        domList = conn.listAllDomains(0)
    except libvirt.libvirtError:
        return 'Failed to list domains.'

    # domainNameList = []
    # for domain in domList:
    #    domainNameList.append(domain.name())

    # Need to do processing on this side and pass object for display in
    # E.g. to catch execption when you try to grab the hostname and your guest
    # VM does not have qemu-guest-agent running

    return render_template('domains/list.html', domains=domList)

