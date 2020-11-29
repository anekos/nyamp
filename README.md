# nyamp
Proxy and Redirector

# Build

```
$ docker build -t nyamp .
```

# Run

```
$ docker run -rm -v /tmp/nyamp:/mnt/cache -p 8000:8080 nyamp
```

```
$ curl 'http://localhost:8000/proxy/https:%2f%2fexample.com/'
<!doctype html>
<html>
...
</html>
```
