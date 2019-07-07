#!/usr/bin/bash

check() {
	require_binaries /usr/sbin/esif_ufd
}

depends() {
	return 0
}

install() {
	inst_multiple /usr/sbin/esif_ufd \
		/usr/share/dptf/ufx64/Dptf.so \
		/usr/share/dptf/ufx64/DptfPolicyActive.so \
		/usr/share/dptf/ufx64/DptfPolicyCritical.so \
		/usr/share/dptf/ufx64/DptfPolicyPassive.so \
		/usr/share/dptf/ufx64/esif_cmp.so \
		/usr/share/dptf/ufx64/esif_ws.so \
		/etc/dptf/dsp.dv \
		/lib/systemd/system/dptf.service

	ln_r /lib/systemd/system/dptf.service /lib/systemd/system/sysinit.target.wants/dptf.service
}
