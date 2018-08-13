Repository name was suggested by github, probably by a random set of words.

## Dependencies

* Python 3
* The python-digitalocean library (https://github.com/koalalorenzo/python-digitalocean)
  ```
  apt install python3-pip
  pip3 install python-digitalocean
  ```
# Ansible Playbook
```
export DO_API_TOKEN="<your Digital Ocean token>"

ansible-playbook -vvvv -i localhost ansible/dropletDeployment.yml
```
# Standalone Python Script
## Listing Digital Ocean Droplets
```
export DO_API_TOKEN="<your Digital Ocean token>"

./python/digitalOceanDroplets.py list
```
## Creating Digital Ocean Droplets

The list of available Digital Ocean size slugs can be found at 
https://developers.digitalocean.com/documentation/changelog/api-v2/new-size-slugs-for-droplet-plan-changes/

```
export DO_API_TOKEN="<your Digital Ocean token>"

./python/digitalOceanDroplets.py create --name "Test" --droplet_size s-1vcpu-1gb
```
### Creating a block storage volume with the Digital Ocean Droplet

The "--volume" flag specifies the size of the block storage in gigabytes.
```
./python/digitalOceanDroplets.py create --name "Test" --droplet_size s-1vcpu-1gb --volume 10
```
### Creating a firewall with the Digital Ocean Droplet
```
./python/digitalOceanDroplets.py create --name "Test" --droplet_size s-1vcpu-1gb --firewall
```

## Creating the block storage volume only

The "--volume" flag specifies the size of the block storage in gigabytes.
```
./python/digitalOceanDroplets.py volume --volume_size 10
```

## Limitations

Some limitations currently are:

 * The "nyc3" region is static
 * The image is set to Ubuntu 18.04 
 * The firewall allows only SSH (Port 22) from anywhere. The code to allow ports 80 and 443 is there, but commented out. 
 * No functionality to attach an existing firewall during the creation of a new droplet
