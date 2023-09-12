from dataclasses import asdict
from quart import jsonify, Blueprint, request
from quart_schema import validate_request
from app.app import app
from quart_jwt_extended import jwt_required

from entities.machine import Machine, MachineInputDTO, MachineUpdateDTO, Machines
from services.files_service import remove_file
import re

from .machines_images import machines_images_router

machines_router = Blueprint('machines', __name__)


def snake_to_camel(s):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), s)


@machines_router.route('/', methods=['POST'])
@validate_request(MachineInputDTO)
@jwt_required
async def create_machine(data: MachineInputDTO):
    """Create a new machine."""
    machine_data_dict = asdict(data)
    purchased_at_without_time_zone = machine_data_dict['purchased_at'].replace(tzinfo=None)
    machine_data_dict['purchased_at'] = purchased_at_without_time_zone
    try:
        id_ = await app.db.fetch_val(
            """SELECT insert_machine( :name, :manufacturer_id, :purchased_at, :year_of_manufacture, 
                               :status, :capacity_in_percent );""",
            values=machine_data_dict,
        )
        result = await app.db.fetch_all(
            """SELECT * from select_single_machine(:id);""",
            values={'id': id_},
        )
        machines = [Machine(**row) for row in result]
        return machines[0].to_json(), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@machines_router.route('/', methods=['PUT'])
@validate_request(MachineUpdateDTO)
@jwt_required
async def update_machine(data: MachineInputDTO):
    """Update a machine."""
    machine_data_dict = asdict(data)
    machine_data_dict['purchased_at'] = machine_data_dict['purchased_at'].replace(tzinfo=None)
    try:
        id_ = await app.db.fetch_val(
            """SELECT update_machine( :id, :name, :manufacturer_id, :purchased_at, :year_of_manufacture, 
                                     :status, :capacity_in_percent );""",
            values=machine_data_dict,
        )
        result = await app.db.fetch_all(
            """SELECT * from select_single_machine(:id);""",
            values={'id': id_},
        )
        machines = [Machine(**row) for row in result]
        return machines[0].to_json(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@machines_router.route('/<int:id>', methods=['DELETE'])
@jwt_required
async def delete_machine(id: int):
    """Delete a machine."""
    try:
        image_url = await app.db.fetch_val(
            """SELECT delete_machine_image_and_get_url( :machine_id );""",
            values={'machine_id': id},
        )
        id_ = await app.db.fetch_val(
            """SELECT * from delete_machine(:id);""",
            values={'id': id},
        )

        if id_ is None:
            return jsonify({'error': 'Machine not found'}), 404
        if image_url is not None:
            remove_file(file_url=image_url, host_url=request.host_url, root_path=app.root_path )
        return '', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@machines_router.route('/', methods=['GET'])
@jwt_required
async def get_machines():
    """Get all machines."""
    result = await app.db.fetch_all(
        """SELECT * from select_all_machines();""",
    )
    machines = [Machine(**row).to_json() for row in result]
    return machines, 200


@machines_router.route('/<int:id>', methods=['GET'])
@jwt_required
async def get_machine(id: int):
    """Get a single machine."""
    result = await app.db.fetch_all(
        """SELECT * from select_single_machine(:id);""",
        values={'id': id},
    )
    machines = [Machine(**row) for row in result]
    if len(machines) == 0:
        return jsonify({'error': 'Machine not found'}), 404
    return machines[0].to_json(), 200

machines_router.register_blueprint(machines_images_router, url_prefix='')
