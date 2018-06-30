install:
	python ./install.py

package:
	tar --exclude='./.git' --exclude='./awspot' --exclude='./specifications' \
			--exclude='./userdata-scripts' -zcvf "awspot-0.1.tar.gz" .
