# PyCA cryptography

https://cryptography.io/en/latest/

## Packaging python-cryptography

The example assumes

* Fedora Rawhide (f34)
* PyCA cryptography release ``3.4``
* Update Bugzilla issues are ``RHBZ#00000001`` and ``RHBZ#00000002``
* Build side tag is ``f34-build-side-12345``

### Request a side tag for building

python-cryptography builds depend on python-cryptography-vectors
package. Both packages must be build in a side tag.

```shell
fedpkg request-side-tag --base-tag f34-build
```

### Build new python-cryptography-vectors first

```shell
pushd ../python-cryptography-vectors
```

Switch and update branch

```shell
fedpkg switch-branch rawhide
fedpkg pull
```

Bump version and get sources

```shell
rpmdev-bumpspec -c "Update to 3.4 (#00000001)" -n 3.4 python-cryptography-vectors.spec
spectool -gf python-cryptography-vectors.spec
```

Upload sources

```shell
fedpkg new-sources cryptography_vectors-3.4.tar.gz
```

Commit changes

```shell
fedpkg commit --clog
fedpkg push
```

Build and wait for repo to regenerate

```shell
fedpkg build --target=f34-build-side-12345
koji wait-repo --build python-cryptography-vectors-3.4-1 f34-build-side-12345
```

### Build new python-cryptography

Switch and update branch

```shell
fedpkg switch-branch rawhide
fedpkg pull
```

Bump version and get sources

```shell
rpmdev-bumpspec -c "Update to 3.4 (#00000002)" -n 3.4 python-cryptography.spec
spectool -gf python-cryptography.spec
```

Upload new sources (**two files!**)

```shell
fedpkg new-sources cryptography-3.4.tar.gz cryptography-3.4.tar.gz.asc
```

Commit changes

```shell
fedpkg commit --clog
fedpkg push
```

Build

```shell
fedpkg build --target=f34-build-side-12345
```
