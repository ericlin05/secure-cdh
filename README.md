# This little project helps user to automate a bunch of CDH component configurations via CM API. Currently the following are supported:

- enable Kerberos (assumes that Kerberos KDC is installed)
- enable Sentry (requires Kerberos to be enabled first
- enable/disable Impala HA
- enable Hive HA
- enable HBase Authentication

Currently when enabling Impala and Hive HA, the HAProxy configuration file will be overwritten each other, I am currently still thinking of a way to fix it.

## Prerequisite

* The following python packages are required to run the script included in the project:

```
pip install pycurl
pip install cm_api
pip install importlib
```

* This also assumes that you have already installed working KDC as well as Kerberos client
on all machines in the cluster. If not, please visit: https://github.com/daisukebe/krb-bootstrap
which includes script to set it up for you.

## How to run

### Get help

```
python main.py -h
```

### Enable Kerberos first

```
python main.py kerberos --cluster-name <cluster-name> \
                        --cm-user <cm-user> \
                        --cm-pass <cm-pass> \
                        <cm-host>
                        <kdc-host>
```

### Enable Sentry (requires Kerberos to be enabled first, need to add checking later on)

```
python main.py sentry --cluster-name <cluster_name> \
                      --cm-user <cm-user> \
                      --cm-pass <cm-pass> \
                      <cm-host>
```

### Enable Impala HA

```
python main.py impala --enable-ha --cluster-name <cluster_name> \
                                  --cm-user <cm-user> \
                                  --cm-pass <cm-pass> \
                                  <cm-host>
```

### Disable Impala HA

```
python main.py impala --disable-ha --cluster-name <cluster_name> \
                                   --cm-user <cm-user> \
                                   --cm-pass <cm-pass> \
                                   <cm-host>
```

### Enable Hive HA

```
python main.py hive --enable-ha --cluster-name <cluster_name> \
                                --cm-user <cm-user> \
                                --cm-pass <cm-pass> \
                                <cm-host>
```

### Enable HBase Authentication

```
python main.py hbase --cluster-name <cluster_name> \
                     --cm-user <cm-user> \
                     --cm-pass <cm-pass> \
                     <cm-host>
```
