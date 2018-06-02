Repository name was suggested by github, probably by a random set of words.

As of 06/02/2018, only the listing of Digital Ocean droplets work.

Dependencies:

* Python 3
* the python-digitalocean library (https://github.com/koalalorenzo/python-digitalocean)
  ```
  apt install python3-pip
  pip3 install python-digitalocean
  ```

Instructions:
```
export DO_API_TOKEN="<your Digital Ocean token>"

./digitalOceanDroplets.py --list
```
