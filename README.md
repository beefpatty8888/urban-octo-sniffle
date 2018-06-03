Repository name was suggested by github, probably by a random set of words.

As of 06/02/2018, only the listing of Digital Ocean droplets work.

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

./digitalOceanDroplets.py --list
```
## Creating Digital Ocean Droplets

The list of available Digital Ocean size slugs can be found at 
https://developers.digitalocean.com/documentation/changelog/api-v2/new-size-slugs-for-droplet-plan-changes/

```
export DO_API_TOKEN="<your Digital Ocean token>"

./digitalOceanDroplets.py --create --size s-1vcpu-1gb
```

