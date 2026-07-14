CVD_FILES:=main.cvd bytecode.cvd daily.cvd safebrowsing.cvd

all: info/init_ok ${CVD_FILES}
	dab bootstrap --minimal
	dab exec sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
	dab cp systemd-presets /etc/systemd/system-preset/00-pve-template.preset
	dab exec touch /proxmox_install_mode
	dab install \
	    antiword \
	    dbus \
	    docx2txt \
	    gpg \
	    ifupdown2 \
	    libcgi-pm-perl \
	    libdbi-perl \
	    libsasl2-modules \
	    odt2txt \
	    perl-openssl-defaults \
	    poppler-utils \
	    proxmox-mailgateway-container \
	    tesseract-ocr \
	    unrtf \
	    ;
	dab exec rm /proxmox_install_mode
	dab exec sed -i '/^deb.*\.proxmox\.com\/.*$$/d;$${/^$$/d;}' /etc/apt/sources.list
	for f in ${CVD_FILES}; do dab cp $$f /var/lib/clamav/$$f; done
	dab finalize --compressor zstd-max

info/init_ok: dab.conf
	dab init
	touch $@

.PHONY: clean
clean:
	dab clean
	rm -f *~

.PHONY: dist-clean
dist-clean: clean
	dab dist-clean
	rm -f ${CVD_FILES}

${CVD_FILES}:
	curl -L --silent --show-error --fail --time-cond $@ --user-agent "CVDUPDATE/0.3.0 (9d591f58-b430-4d0c-99b2-febb1cee0872)" -o $@.tmp https://database.clamav.net/$@
	[ -f $@.tmp ] && mv $@.tmp $@ || true
	if command -v sigtool > /dev/null ; then sigtool -i $@; else echo "skipping verification of $@"; fi
