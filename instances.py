import boto3
import csv

def GetName(resource):
    if "Tags" in resource.keys():
        for tag in resource.get("Tags"):
            if tag.get("Key") == "Name":
                return tag.get("Value")

session = boto3.Session(profile_name="ApplicationEUProd", region_name="us-east-2")
ec2 = session.client("ec2")


def GetInstances():
    result = []
    for reservation in ec2.describe_instances()["Reservations"]:
        for instance in reservation["Instances"]:            
            
            description = {
                "Name":             GetName(instance),
                "PrivateIpAddress": instance["PrivateIpAddress"],
                "InstanceId":       instance["InstanceId"],
                "InstanceType":     instance["InstanceType"],
                "SubnetId":         instance["SubnetId"],
                "AvailabilityZone": instance["Placement"]["AvailabilityZone"]
                }

            result.append(description)
    
    return result


with open('Instances.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(["Name" + "," + "PrivateIpAddress" + "," + "InstanceId" + "," + "InstanceType" + "," + "SubnetId" + "," + "AvailabilityZone"])
    for instance in GetInstances():
        writer.writerow([instance["Name"] + "," + instance["PrivateIpAddress"] + "," + instance["InstanceId"] + "," + instance["InstanceType"] + "," + instance["SubnetId"] + "," + instance["AvailabilityZone"]])
