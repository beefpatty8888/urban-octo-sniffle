Repository name was suggested by github, probably by a random set of words.

## Dependencies

* Python 3
* The python-digitalocean library (https://github.com/koalalorenzo/python-digitalocean)
  ```
  apt install python3-pip
  pip3 install python-digitalocean
  ```

## Listing Digital Ocean Droplets
```
export DO_API_TOKEN="<your Digital Ocean token>"

./digitalOceanDroplets.py list
```
## Creating Digital Ocean Droplets

The list of available Digital Ocean size slugs can be found at 
https://developers.digitalocean.com/documentation/changelog/api-v2/new-size-slugs-for-droplet-plan-changes/

```
export DO_API_TOKEN="<your Digital Ocean token>"

./digitalOceanDroplets.py create --name "Test" --droplet_size s-1vcpu-1gb
```
### Creating a block storage volume with the Digital Ocean Droplet

The "--volume" flag specifies the size of the block storage in gigabytes.
```
./digitalOceanDroplets.py create --name "Test" --droplet_size s-1vcpu-1gb --volume 10
```

## Creating the block storage volume only

The "--volume" flag specifies the size of the block storage in gigabytes.
```
./digitalOceanDroplets.py volume --volume_size 10
```

## Limitations

Some limitations currently are:

 * The "nyc3" region is static
 * The image is set to Ubuntu 18.04 
