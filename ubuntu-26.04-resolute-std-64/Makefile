BASEDIR:=$(shell dab basedir)

all: info/init_ok
	dab bootstrap
	mkdir -p $(BASEDIR)/usr/lib/systemd/system/netplan-configure.service.d
	printf '# PVE: avoid udev trigger in container\n[Service]\nExecStartPost=\n' \
	  | tee $(BASEDIR)/usr/lib/systemd/system/netplan-configure.service.d/override.conf
	mkdir -p $(BASEDIR)/etc/systemd/system-preset
	echo "disable chrony-wait.service" >$(BASEDIR)/etc/systemd/system-preset/00-pve-template.preset
	###
	# NOTE: zstd appliances are only supported on PVE >= 7.0, take care on upload!
	###
	dab finalize --compressor zstd-max

info/init_ok: dab.conf
	dab init
	touch $@

.PHONY: clean
clean:
	dab clean
	rm -f *~

.PHONY: dist-clean
dist-clean:
	dab dist-clean
	rm -f *~

upload: TARGET=$(shell dab targetname)
upload:
	tar cf - $(TARGET).* | ssh repoman upload --type apl --dist bookworm
