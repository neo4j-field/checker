import sys
import pandas
import pyarrow as pa

from graphdatascience import GraphDataScience
from graphdatascience.graph.graph_object import Graph

_checks = {
    "Ex 01": {
        "Task 1": {
            "gds": {
                "type": GraphDataScience,
                "eval": "gds.version()",
            },
        },
        "Task 2": {
            "users": {
                "type": pandas.DataFrame,
                "eval": "users.shape == (33732, 3) and list(users.columns) == ['nodeId', 'fraudMoneyTransfer', 'labels']",
            },
        },
        "Task 3": {
            "referred": {
                "type": pandas.DataFrame,
                "eval": "referred.shape == (1870, 3) and list(referred.columns) == ['sourceNodeId', 'targetNodeId', 'relationshipType']",
            },
        },
        "Task 4": {
            "G": {
                "type": Graph,
                "eval": "G.name() == 'Exercise-01' and G.node_count() == 33732 and G.relationship_count() == 1870 and G.node_labels() == ['User'] and G.relationship_types() == ['REFERRED']",
            },
        },
        "Task 5": {
            "wcc_components": {
                "type": int,
                "eval": "wcc_components == 31909",
            },
        },
        "Bonus": {
            "top10": {
                "type": pandas.DataFrame,
                "eval": "top10.shape == (10, 1) and top10.values.flatten().tolist() == [7, 7, 7, 7, 6, 5, 5, 5, 5, 5]"
            },
        },
    },
    "Ex 02": {
        "Task 1": {
            "G": {
                "type": Graph,
                "eval": "G.node_labels() == ['User', 'IP'] and G.relationship_types() == ['HAS_IP', 'SIMILAR_BY_IP'] and G.relationship_properties()['SIMILAR_BY_IP'] == ['score']",
            },
        },
        "Task 2": {
            "G": {
                "type": Graph,
                "eval": "G.node_labels() == ['User', 'IP'] and G.relationship_types() == ['HAS_IP', 'SIMILAR_BY_IP'] and 'fastRP' in G.node_properties()['User']",
            },
        },
        "Task 3": {
            "df": {
                "type": pandas.DataFrame,
                "eval": "df.shape == (619587, 2) and (list(df.columns) == ['nodeId', 'propertyValue'] or list(df.columns) == ['nodeId', 'fastRP'])",
            },
        },
    },
    "Ex 03": {
        "Task 1": {
            "referred": {
                "type": pa.Table,
                "eval": "referred.column_names == ['sourceNodeId', 'targetNodeId', 'relationshipType'] and referred.num_rows == 1870"
            },
        },
        "Task 2": {
            "result": {
                "type": tuple,
                "eval": "result == (1870, 52832)"
            },
        },
        "Task 3": {
            "result": {
                "type": dict,
                "eval": "result == {'name': 'Exercise-03', 'relationship_count': 1870 }"
            },
        },
    },
    "Ex 04": {
        "Task 1": {
            "users": {
                "type": pa.Table,
                "eval": "users.column_names == ['nodeId', 'fraudMoneyTransfer', 'labels'] and users.num_rows == 33732"
            },
            "ips": {
                "type": pa.Table,
                "eval": "'nodeId' in ips.column_names and 'labels' in ips.column_names and ips.num_rows == 585855"
            },
            "has_ip": {
                "type": pa.Table,
                "eval": "has_ip.column_names == ['sourceNodeId', 'targetNodeId', 'relationshipType'] and has_ip.num_rows == 1488949"
            },
        },
        "Task 2": {
            "users_results": {
                "type": tuple,
                "eval": "users_results[0] == 33732 and users_results[1] > 1"
            },
            "ips_results": {
                "type": tuple,
                "eval": "ips_results[0] == 585855 and ips_results[1] > 1"
            },
        },
        "Task 3": {
            "result": {
                "type": dict,
                "eval": "result == {'name': 'Exercise-04', 'node_count': 619587}",
            },
        },
        "Task 4": {
            "result": {
                "type": tuple,
                "eval": "result[0] == 1488949 and result[1] > 1"
            },
        },
        "Task 5": {
            "result": {
                "type": dict,
                "eval": "result == {'name': 'Exercise-04', 'relationship_count': 1488949}"
            },
        },
    },
}

def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def check_result(exercise: str, task: str, **kwargs):
    try:
        ex = _checks.get(exercise, None)
        if ex is None:
            raise Exception(f"invalid exercise '{exercise}'")
            
        check = ex.get(task, None)
        if check is None:
            raise Exception(f"invalid task '{task}'")
            
        for key in check:
            subcheck = check.get(key, {})
            obj = kwargs.get(key, None)
            if obj is None:
                raise Exception(
                    f"can't find {key} in kwargs! ({list(kwargs.keys())})")
            
            _type = subcheck.get("type", object)
            code = subcheck.get("eval", "True")
            
            if not isinstance(obj, _type):
                raise Exception(f"{key} should be of type {_type.__name__}")
            if not bool(eval(code, None, {key: obj})):
                raise Exception(f"Failed test check on {key}. Go check your work!")
        print(f"🥳 {exercise}/{task} passed!")
    except Exception as e:
        error(f"🚨 {exercise}/{task} failed 😭\n------------------------\n{e}")
    