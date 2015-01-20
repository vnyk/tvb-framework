# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2013, Baycrest Centre for Geriatric Care ("Baycrest")
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Launch an operation from the command line

.. moduleauthor:: Lia Domide <lia.domide@codemart.ro>
"""

if __name__ == "__main__":
    from tvb.basic.profile import TvbProfile
    TvbProfile.set_profile(TvbProfile.COMMAND_PROFILE)

from tvb.core.entities.storage import dao
from tvb.core.services.flow_service import FlowService
from tvb.adapters.uploaders.tvb_importer import TVBImporter


## Before starting this, we need to have TVB web interface launched at least once (to have a default project, user, etc)
def import_h5(file_path, project_id):

    flow_service = FlowService()

    ## This ID of a project needs to exists in Db, and it can be taken from the WebInterface:
    project = dao.get_project_by_id(project_id)

    adapter_instance = TVBImporter()
    my_group = dao.find_group(TVBImporter.__module__, TVBImporter.__name__)
    adapter_instance.algorithm_group = my_group

    ## Prepare the input algorithms as if they were coming from web UI submit:
    launch_args = {"data_file": file_path}

    print "We will try to import file at path " + file_path
    ## launch an operation and have the results stored both in DB and on disk
    launched_operations = flow_service.fire_operation(adapter_instance,
                                                      project.administrator,
                                                      project.id,
                                                      **launch_args)

    print "Operation launched. Check the web UI"