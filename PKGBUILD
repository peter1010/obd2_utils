pkgbase=py_obd2_utils
pkgname=('obd2_utils')
pkgver=1.0
pkgrel=5
pkgdesc="OBD2 utils"
arch=('any')
url="http:"
license=('GPL')
makedepends=('python')
depends=('python')
source=()

pkgver() {
    python ../setup.py -V
}

check() {
    pushd ..
    python setup.py check
    popd
}

package() {
    pushd ..
    python setup.py install --root=$pkgdir
    popd
}

