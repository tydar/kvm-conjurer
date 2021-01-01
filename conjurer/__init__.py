import os
import libvirt

from flask import Flask

def create_app(test_config=None):
    # create and configure the Flask app object
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'conjurer.sqlite'),
    )

    if test_config is None:
        # load the instance config file when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if we get it
        app.config.from_mapping(test_config)

    # insure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello_world():
        return 'Hello, World!'

    # page that should list libvirt VMs
    @app.route('/list')
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

        domainNameList = []
        for domain in domList:
            domainNameList.append(domain.name())

        return str(domainNameList)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import domains
    app.register_blueprint(domains.bp)

    return app
