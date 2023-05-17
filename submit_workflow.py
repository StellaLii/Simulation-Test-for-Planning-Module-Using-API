import argparse
from unittest import skip
import requests
import json
import time
from copy import deepcopy


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


WORKFLOW_URL_TEMPLATE = ""
ARCHIVED_WORKFLOW_URL_TEMPLATE = ""

GET_SCENARIO_RESULTS_URL = ""
SUBMIT_WORKFLOW_URL = ""
LIST_SCENARIOS_URL = ""
LIST_SCENARIOS_BY_ID_URL = ""
ARGO_SERVER_URL = ""
GET_RESOLVED_SCENARIOS_URL = ""

SINGLE_FRAME_TEMPLATE_GENERAL = "planning-cicd-single-frame-test-2-2-0"
SINGLE_FRAME_TEMPLATE_NO_INCIDENT_TIME = (
    "planning-cicd-single-frame-no-incident-time-1-0-0"
)
SINGLE_FRAME_TEMPLATE_COMPARE = "planning-cicd-direct-single-frame-compare-2-1-1"
SINGLE_FRAME_TEMPLATE_REINSTALL_PLANNING = (
    "planning-cicd-single-frame-test-reinstall-1-0-0"
)

CHECK_MODE = "Failed"
BASELINE_PLANNING_PREDICTION_VERSIONS = []


class WorkflowInfo:
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid


class ScenarioInfo:
    def __init__(self, id):
        self.id = id


def show_workflow_info(submit_single_frame_task_response,
                       planning_version,
                       compare_version=""):
    workflow_info = submit_single_frame_task_response.json()
    workflow_name = workflow_info["metadata"]["name"]
    workflow_uid = workflow_info["metadata"]["uid"]
    current_argo_servier_url = ARGO_SERVER_URL + "/" + workflow_name
    print("------------------------------------------------------------")
    print("Planning Version: " + planning_version)
    if compare_version:
        print("Compare Version: " + compare_version)
    print("Workflow Name: " + workflow_name)
    print("Workflow UID: " + workflow_uid)
    print(bcolors.OKGREEN + "Single frame task submitted successfully!" +
          bcolors.ENDC)
    print(bcolors.OKGREEN + "Check out the running status in: " +
          current_argo_servier_url + bcolors.ENDC)

    return WorkflowInfo(workflow_name, workflow_uid)


def submit_task_only_single_frame_compare_task(request_body_list):
    try:
        submit_single_frame_task_response = requests.post(
            SUBMIT_WORKFLOW_URL,
            json={
                "resourceKind": "WorkflowTemplate",
                "resourceName": SINGLE_FRAME_TEMPLATE_COMPARE,
                "submitOptions": {
                    "labels":
                    "creator=planning_ci",
                    "parameters": [
                        "COMPARE_VERSION=" + request_body_list["COMPARE_VERSION"],
                        "PLANNING_VERSION=" + request_body_list["PLANNING_VERSION"],
                        "SCENARIOS_COMMIT_ID="
                        + request_body_list["SCENARIOS_COMMIT_ID"],
                        "SCENARIOS="
                        + json.dumps(
                            request_body_list["SCENARIOS"]
                            + request_body_list["WORLD_SIM_SCENARIOS"],
                            separators=(",", ":"),
                        ),
                        "SINGLE_FRAME_TASK_IMAGE_NAME="
                        + request_body_list["SINGLE_FRAME_TASK_IMAGE_NAME"],
                    ],
                },
            },
        )
        submit_single_frame_task_response.raise_for_status()

    except requests.RequestException as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        print(
            bcolors.FAIL + str(submit_single_frame_task_response.content) + bcolors.ENDC
        )
        print(bcolors.FAIL + "submit single frame task failed!" + bcolors.ENDC)
        exit(1)

    return show_workflow_info(
        submit_single_frame_task_response,
        request_body_list["PLANNING_VERSION"],
        request_body_list["COMPARE_VERSION"],
    )


def submit_single_frame_task(template_name, request_body_list):
    try:
        submit_single_frame_task_response = requests.post(
            SUBMIT_WORKFLOW_URL,
            json={
                "resourceKind": "WorkflowTemplate",
                "resourceName": template_name,
                "submitOptions": {
                    "labels":
                    "creator=planning_ci",
                    "parameters": [
                        "PLANNING_VERSION=" + request_body_list["PLANNING_VERSION"],
                        "PLANNING_REF_NAME=" + request_body_list["PLANNING_REF_NAME"],
                        "PLANNING_COMMIT_ID=" + request_body_list["PLANNING_COMMIT_ID"],
                        "SCENARIOS_COMMIT_ID="
                        + request_body_list["SCENARIOS_COMMIT_ID"],
                        "SCENARIOS="
                        + json.dumps(
                            request_body_list["SCENARIOS"]
                            + request_body_list["WORLD_SIM_SCENARIOS"],
                            separators=(",", ":"),
                        ),
                        "SINGLE_FRAME_TASK_IMAGE_NAME="
                        + request_body_list["SINGLE_FRAME_TASK_IMAGE_NAME"],
                        "CHECK_MODE=" + CHECK_MODE,
                    ],
                },
            },
        )
        submit_single_frame_task_response.raise_for_status()
    except requests.RequestException as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        print(
            bcolors.FAIL + str(submit_single_frame_task_response.content) + bcolors.ENDC
        )
        print(bcolors.FAIL + "submit single frame task failed!" + bcolors.ENDC)
        exit(1)

    return show_workflow_info(submit_single_frame_task_response,
                              request_body_list["PLANNING_VERSION"])


def is_workflow_complete(workflow_json):
    if "phase" not in workflow_json["status"]:
        return False

    workflow_status = str(workflow_json["status"]["phase"])
    if workflow_status == "Failed" or workflow_status == "Succeeded":
        archived_workflow_info_url = ARCHIVED_SERVER_URL + (
            workflow_json["metadata"]["uid"]
            if workflow_json["metadata"]["uid"] is not None else "")
        print(bcolors.OKGREEN + "Check out the finished status in: " +
              archived_workflow_info_url + bcolors.ENDC)
        return True
    return False


def get_workflow_json(uid, name):
    workflow_url = WORKFLOW_URL_TEMPLATE + name
    archived_workflow_url = ARCHIVED_WORKFLOW_URL_TEMPLATE + uid

    # get workflow json from workflows list
    get_workflow_response = requests.get(workflow_url)
    if get_workflow_response.status_code == 200:
        return get_workflow_response.json()

    # get workflow json from archived workflows list
    try:
        get_archived_workflow_response = requests.get(archived_workflow_url)
        get_archived_workflow_response.raise_for_status()
    except requests.RequestException as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        print(bcolors.FAIL + "get archived workflow status failed!" +
              bcolors.ENDC)
        exit(1)

    archived_workflow_json = get_archived_workflow_response.json()
    return archived_workflow_json


def submit_single_frame_tasks(test_mode, use_baseline_version, request_body_lists):
    workflows_json = {}
    workflows_json["test_mode"] = test_mode
    workflows_json["workflows"] = []
    for request_body_list in request_body_lists:
        if test_mode == "compare":
            workflow_info = submit_task_only_single_frame_compare_task(
                request_body_list)
        elif test_mode == "all":
            workflow_info = submit_single_frame_task(
                SINGLE_FRAME_TEMPLATE_NO_INCIDENT_TIME, request_body_list
            )
        elif test_mode == "pending" or use_baseline_version == "yes" or test_mode == "grading_ready_with_history_ppnode_versions":
            workflow_info = submit_single_frame_task(
                SINGLE_FRAME_TEMPLATE_REINSTALL_PLANNING, request_body_list
            )
        else:
            workflow_info = submit_single_frame_task(
                SINGLE_FRAME_TEMPLATE_GENERAL, request_body_list)

        workflow_json = {}
        workflow_json["uid"] = workflow_info.uid
        workflow_json["name"] = workflow_info.name
        workflow_json["planning_version"] = request_body_list[
            "PLANNING_VERSION"]
        workflow_json["scenarios"] = request_body_list["SCENARIOS"]
        workflow_json["world_sim_scenarios"] = request_body_list[
            "WORLD_SIM_SCENARIOS"]

        workflows_json["workflows"].append(workflow_json)

        if len(request_body_lists) > 2:
            while True:
                workflow_status = get_workflow_json(workflow_json["uid"],
                                                    workflow_json["name"])
                if is_workflow_complete(workflow_status):
                    break
                time.sleep(60)

    with open("/tmp/workflow_info.json", "w") as f:
        json.dump(workflows_json, f)


def get_other_module_versions_from_config_file(module_versions_config_file):
    module_versions = {}
    with open(module_versions_config_file, "r") as f:
        module_versions = json.load(f)

        module_versions["SCENARIOS_BRANCH"] = str(
            module_versions["SCENARIOS_REPO"] + module_versions["SCENARIOS_BRANCH"],
        )
        # in case scenarios commit id not exist
        if "SCENARIOS_COMMIT_ID" not in module_versions:
            module_versions["SCENARIOS_COMMIT_ID"] = ""

        global BASELINE_PLANNING_PREDICTION_VERSIONS
        BASELINE_PLANNING_PREDICTION_VERSIONS = module_versions[
            "BASELINE_PLANNING_PREDICTION_VERSIONS"
        ]

    return module_versions


def get_scenario_list_from_config_file(scenario_list_file, field):
    scenario_list = []
    with open(scenario_list_file, "r") as f:
        file_content = json.load(f)
        if field not in file_content:
            print(
                bcolors.FAIL
                + "invalid planning resolved scenario list file! '"
                + field
                + "' required!"
                + bcolors.ENDC
            )
            return scenario_list
        scenario_list = file_content[field]

    return scenario_list


def list_scenarios_from_scenarios_db(request_payloads):
    scenarios = []

    while True:
        try:
            list_scenarios_response = requests.get(
                LIST_SCENARIOS_URL,
                json=request_payloads,
            )
            list_scenarios_response.raise_for_status()
            if list_scenarios_response.status_code == 200:
                break
        except requests.RequestException as e:
            print(bcolors.FAIL + str(e) + bcolors.ENDC)
            print(bcolors.FAIL + str(list_scenarios_response.content) +
                  bcolors.ENDC)
            print(bcolors.WARNING + "retry request" + bcolors.ENDC)

        time.sleep(30)

    returned_scenarios = list_scenarios_response.json()
    if ("scenarios" in returned_scenarios
            and len(returned_scenarios["scenarios"]) > 0
            and "version" in returned_scenarios["scenarios"][0]):
        scenarios = returned_scenarios["scenarios"]

    return scenarios


def list_scenarios_from_db_by_ids(request_payloads):
    scenarios = []

    try:
        list_scenarios_response = requests.get(
            LIST_SCENARIOS_BY_ID_URL,
            json=request_payloads,
        )
        list_scenarios_response.raise_for_status()
    except requests.RequestException as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        print(bcolors.FAIL + str(list_scenarios_response.content) + bcolors.ENDC)
        print(bcolors.FAIL + "list scenarios by id failed" + bcolors.ENDC)
        exit(1)

    returned_scenarios = list_scenarios_response.json()
    if (
        "scenarios" in returned_scenarios
        and len(returned_scenarios["scenarios"]) > 0
        and "version" in returned_scenarios["scenarios"][0]
    ):
        scenarios = returned_scenarios["scenarios"]

    return scenarios


def get_all_scenarios(request_payloads):
    returned_scenarios = list_scenarios_from_scenarios_db(request_payloads)
    return returned_scenarios


def get_stable_scenarios(request_payloads):
    request_payloads["grading_ready"] = "TRUE"
    request_payloads["stable"] = "TRUE"
    returned_scenarios = list_scenarios_from_scenarios_db(request_payloads)
    return returned_scenarios


def get_unstable_scenarios(request_payloads):
    request_payloads["grading_ready"] = "TRUE"
    request_payloads["stable"] = "FALSE"
    returned_scenarios = list_scenarios_from_scenarios_db(request_payloads)
    return returned_scenarios


def get_resolved_scenarios(request_payloads):
    resolved_scenario_id_list = get_scenario_list_from_config_file(
        "./gitlab_ci/single_frame/scenario_list/resolved_scenario_list.json",
        "resolved_scenario_id_list",
    )

    request_payloads["scenario_ids"] = resolved_scenario_id_list
    returned_scenarios = list_scenarios_from_db_by_ids(request_payloads)
    return returned_scenarios


def get_pending_scenarios(request_payloads):
    pending_scenario_id_list = get_scenario_list_from_config_file(
        "./gitlab_ci/single_frame/scenario_list/pending_scenario_list.json",
        "pending_scenario_id_list",
    )

    request_payloads["scenario_ids"] = pending_scenario_id_list
    returned_scenarios = list_scenarios_from_db_by_ids(request_payloads)
    return returned_scenarios


def get_specified_list_scenarios(request_payloads):
    specified_scenaio_id_list = get_scenario_list_from_config_file(
        # "./gitlab_ci/single_frame/scenario_list/specified_list.json",
        # "specified_scenaio_id_list",
        "/home/DEEPROUTE/jiananli/simapitest/JSON_List/specified_list.json"
    )

    request_payloads["scenario_ids"] = specified_scenaio_id_list
    returned_scenarios = list_scenarios_from_db_by_ids(request_payloads)
    return returned_scenarios



def get_grading_ready_scenarios(request_payloads):
    request_payloads["grading_ready"] = "TRUE"
    returned_scenarios = list_scenarios_from_scenarios_db(request_payloads)

    return returned_scenarios


def get_normal_scenarios(request_payloads):
    request_payloads["grading_ready"] = "TRUE"
    request_payloads["issue_types"] = ["NORMAL"]
    returned_scenarios = list_scenarios_from_scenarios_db(request_payloads)

    return returned_scenarios


def get_scenario_contents_by_metadata(scenario_metadata_list):
    scenario_uids = []
    for curr_scenario in scenario_metadata_list:
        scenario_uids.append(curr_scenario["scenarioUid"])

    try:
        get_scenarios_content_response = requests.post(
            GET_SCENARIOS_CONTENT_URL,
            json={
                "scenario_uids": scenario_uids,
            },
        )
        get_scenarios_content_response.raise_for_status()
    except requests.RequestException as e:
        print(bcolors.FAIL + str(e) + bcolors.ENDC)
        print(bcolors.FAIL + "get scenario content failed" + bcolors.ENDC)

    return get_scenarios_content_response.json()["scenarios"]


def get_scenario_by_test_mode_and_scenarios_branch(
    test_mode, scenarios_branch, scenarios_commit_id, scenario_list_root
):
    request_payloads = {
        "group_name": scenarios_branch,
        "version": scenarios_commit_id,
    }

    switch = {
        "all": get_all_scenarios,
        "stable": get_stable_scenarios,
        "unstable": get_unstable_scenarios,
        "resolved": get_resolved_scenarios,
        "pending": get_pending_scenarios,
        "specified_list": get_specified_list_scenarios,
        "normal": get_normal_scenarios,
        "compare": get_stable_scenarios,
        "grading_ready": get_grading_ready_scenarios,
        "grading_ready_with_history_ppnode_versions": get_grading_ready_scenarios,
    }
    returned_scenarios = switch[test_mode](request_payloads)
    if len(returned_scenarios) == 0:
        print(bcolors.FAIL + "no such scenarios found!" + bcolors.ENDC)
        exit(1)

    updated_scenarios_commit_id = returned_scenarios[0]["version"]

    scenarios = []
    world_sim_scenarios = []
    returned_scenario_contents = get_scenario_contents_by_metadata(returned_scenarios)

    for key, value in returned_scenario_contents.items():
        curr_scenario_uid = key
        curr_scenario_content = json.loads(value)
        curr_scenario_id = curr_scenario_content["metadata"]["scenario_id"]

        activate_open_loop = ("grading_config" in curr_scenario_content
                              and "open_loop_grading_config"
                              in curr_scenario_content["grading_config"])
        activate_close_loop = ("grading_config" in curr_scenario_content
                               and "close_loop_grading_config"
                               in curr_scenario_content["grading_config"])

        # If we are not running "all scenarios" job, we jump the unfinished scenarios.
        if test_mode != "all" and "log_sim_config" in curr_scenario_content:
            if (
                "incident_start_time" not in curr_scenario_content["log_sim_config"]
                or "incident_duration" not in curr_scenario_content["log_sim_config"]
            ):
                continue

        # If we are not running "all normal" job, we jump all the normal scenario cases.
        if (
            test_mode != "normal"
            and "issue_types" in curr_scenario_content["metadata"]
            and "NORMAL" in curr_scenario_content["metadata"]["issue_types"]
        ):
            continue

        scenario = {}
        scenario["scenario_id"] = curr_scenario_id
        scenario["scenario_uid"] = curr_scenario_uid
        if activate_open_loop:
            # scenario["play_mode"] = "OpenLoop"
            # scenarios.append(deepcopy(scenario))
            skip
        if activate_close_loop:
            if "world_sim_config" in curr_scenario_content:
                scenario["play_mode"] = "WorldSim"
                world_sim_scenarios.append(deepcopy(scenario))
            else:
                scenario["play_mode"] = "CloseLoop"
                scenarios.append(deepcopy(scenario))
        if not (activate_close_loop or activate_open_loop):
            scenario["play_mode"] = "CloseLoop"
            scenarios.append(deepcopy(scenario))

    return scenarios, world_sim_scenarios, updated_scenarios_commit_id


def get_request_body_lists(args):
    request_body_list = get_other_module_versions_from_config_file(
        args.module_versions_config_file)
    if args.single_frame_task_image_name:
        request_body_list[
            "SINGLE_FRAME_TASK_IMAGE_NAME"
        ] = args.single_frame_task_image_name

    (
        scenarios,
        world_sim_scenarios,
        updated_scenarios_commit_id,
    ) = get_scenario_by_test_mode_and_scenarios_branch(
        args.test_mode,
        request_body_list["SCENARIOS_BRANCH"],
        request_body_list["SCENARIOS_COMMIT_ID"],
        args.scenario_list_root
    )
    print(bcolors.OKBLUE + "Scenarios Commit id: " +
          str(updated_scenarios_commit_id) + bcolors.ENDC)
    print(bcolors.OKBLUE + "Number of Scenarios To Be Submitted: " +
          str(len(scenarios)) + bcolors.ENDC)
    print(bcolors.OKBLUE + "Number of WorldSim Scenarios To Be Submitted: " +
          str(len(world_sim_scenarios)) + bcolors.ENDC)

    # scenarios_commit_id will be updated to the actual value here if it was originally be "", which means we
    # want the most updated version of the specific branch
    request_body_list["SCENARIOS_COMMIT_ID"] = updated_scenarios_commit_id

    request_body_list["PLANNING_VERSION"] = args.planning_version
    request_body_list["PLANNING_REF_NAME"] = (
        args.planning_ref_name if args.planning_ref_name else ""
    )
    request_body_list["PLANNING_COMMIT_ID"] = (
        args.planning_commit_id if args.planning_commit_id else ""
    )

    request_body_lists = []
    batch_scenarios = []
    exist_batch_py_planning = set()
    if args.test_mode == "all" or args.test_mode == "grading_ready":
        while len(scenarios) > 0:
            batch_scenarios.append(scenarios.pop(0))
            if len(batch_scenarios) == 2000 or len(scenarios) == 0:
                curr_request_body_list = dict(request_body_list)
                curr_request_body_list["SCENARIOS"] = deepcopy(batch_scenarios)
                curr_request_body_list["WORLD_SIM_SCENARIOS"] = (
                    world_sim_scenarios
                    if len(request_body_lists) == 0 else [])
                request_body_lists.append(curr_request_body_list)
                batch_scenarios = []
    elif args.test_mode == "pending" or args.test_mode == "grading_ready_with_history_ppnode_versions":
        BASELINE_PLANNING_PREDICTION_VERSIONS.insert(0, args.planning_version)
        for curr_planning_version in BASELINE_PLANNING_PREDICTION_VERSIONS:
            copy_scenarios = deepcopy(scenarios)
            while len(copy_scenarios) > 0:
                batch_scenarios.append(copy_scenarios.pop(0))
                if len(batch_scenarios) == 2000 or len(copy_scenarios) == 0:
                    curr_request_body_list = dict(request_body_list)
                    curr_request_body_list["PLANNING_VERSION"] = curr_planning_version
                    curr_request_body_list["SCENARIOS"] = deepcopy(batch_scenarios)
                    curr_request_body_list["WORLD_SIM_SCENARIOS"] = (
                        world_sim_scenarios if curr_planning_version not in exist_batch_py_planning else []
                    )
                    # TODO(jingwei): different versions of planning should have different ref_name, commit id
                    # and resolved scenarios list, should fix later
                    request_body_lists.append(curr_request_body_list)
                    exist_batch_py_planning.add(curr_planning_version)
                    batch_scenarios = []
    else:
        request_body_list["SCENARIOS"] = scenarios
        request_body_list["WORLD_SIM_SCENARIOS"] = world_sim_scenarios
        request_body_lists.append(request_body_list)

    return request_body_lists


def config_service_url(namespace):
    global WORKFLOW_URL_TEMPLATE
    WORKFLOW_URL_TEMPLATE = (
        "http://argo-prod.aliyun.simulation.deeproute.net/api/v1/workflows/{}/"
        .format(namespace, namespace))

    global ARCHIVED_WORKFLOW_URL_TEMPLATE
    ARCHIVED_WORKFLOW_URL_TEMPLATE = "http://argo-prod.aliyun.simulation.deeproute.net/api/v1/archived-workflows/".format(
        namespace)

    global ARCHIVED_SERVER_URL
    ARCHIVED_SERVER_URL = "http://argo-prod.aliyun.simulation.deeproute.net/archived-workflows/{}/".format(
        namespace, namespace)

    global LIST_SCENARIOS_URL
    LIST_SCENARIOS_URL = (
        "http://scenario-service.{}.simulation.deeproute.ai/api/v2/scenarios".
        format(namespace))

    global SUBMIT_WORKFLOW_URL
    SUBMIT_WORKFLOW_URL = "http://argo-prod.aliyun.simulation.deeproute.net/api/v1/workflows/{}/submit".format(
        namespace)

    global GET_SCENARIOS_CONTENT_URL
    GET_SCENARIOS_CONTENT_URL = "http://scenario-service.{}.simulation.deeproute.ai/api/v2/get_scenarios_content".format(
        namespace)

    global ARGO_SERVER_URL
    ARGO_SERVER_URL = (
        "http://argo-prod.aliyun.simulation.deeproute.net/workflows/{}".format(
            namespace))

    global LIST_SCENARIOS_BY_ID_URL
    LIST_SCENARIOS_BY_ID_URL = "http://scenario-service.{}.simulation.deeproute.ai/api/v2/list_scenarios_by_id".format(
        namespace
    )


def do_dry_run(request_body_lists):
    print(bcolors.OKGREEN + str(len(request_body_lists)) +
          " workflows to be submitted." + bcolors.ENDC)
    for request_body_list in request_body_lists:
        submit_single_frame_test_task_summmary = {
            "request_body_list": request_body_list
        }
        print(json.dumps(
            submit_single_frame_test_task_summmary,
            indent=4,
            sort_keys=True,
        ))
    return


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", default="simulation-platform-prod")
    parser.add_argument("--planning_version", required=True)
    parser.add_argument("--planning_ref_name")
    parser.add_argument("--planning_commit_id")
    parser.add_argument(
        "--test_mode",
        choices=[
            "all",
            "stable",
            "unstable",
            "resolved",
            "compare",
            "pending",
            "specified_list",
            "normal",
            "grading_ready",
            "grading_ready_with_history_ppnode_versions",
        ],
        # default="specified_list",
        default="grading_ready",
    )
    parser.add_argument(
        "--resolved_scene_list_file",
        default="./gitlab_ci/single_frame/resolved_scene_list.json",
    )
    parser.add_argument(
        "--module_versions_config_file",
        default=
        "./gitlab_ci/single_frame/task_image/module_versions_config.json",
    )
    parser.add_argument(
        "--scenario_list_root",
        default="./gitlab_ci/single_frame/scenario_list/"
    )
    parser.add_argument("--single_frame_task_image_name", required=True)
    parser.add_argument("--use_baseline_version", default="not_use")

    parser.add_argument("--check_mode", choices=["Failed", "Crashed"], default="Failed")

    parser.add_argument("--dry_run", action="store_true")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    config_service_url(args.namespace)

    request_body_lists = get_request_body_lists(args)

    if args.dry_run:
        do_dry_run(request_body_lists)
        exit(0)

    CHECK_MODE = args.check_mode
    submit_single_frame_tasks(
        args.test_mode, args.use_baseline_version, request_body_lists
    )

    exit(0)
