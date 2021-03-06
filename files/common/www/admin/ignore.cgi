#!/bin/sh

. /lib/functions.sh

export TITLE="Verwaltung > Konfiguration: Knoten ignorieren"
. /usr/lib/www/page-pre.sh ${0%/*}

cat<<EOM
<h2>$TITLE</h2>
<br>

Hier k&ouml;nnen benachbarte Knoten gespeichert werden, die vom Routing-Protokoll
ignoriert werden sollen. Dabei werden nur Routing-Informationen ignoriert, welche via WiFi (Ad-hoc) empfangen werden.<br>
Sind zwei Knoten in WiFi-Reichweite und gleichzeitig &uuml;ber das Backbone (LAN) miteinander verbunden,
kann hiermit die zus&auml;tzliche, in der Regel unn&ouml;tige, Verbindung via WiFi unterbunden werden.<br>
Die Einstellungen sind erst nach einem Neustart aktiv.<br><br>
EOM

display_ignored_nodes() {
cat<<EOM

<fieldset class="bubble">
<legend>Gespeicherte Knoten</legend>
<table>

<tr><th width="100">Knoten</th><th></th></tr>
EOM

T=1
C=0
print_node() {
	if [ -n "$1" ]; then
		echo "<tr class=\"colortoggle$T\" ><td width=\"100\">$1</td>"
		echo "<td valign=bottom><FORM name=\"form_node_del_"$C"\" ACTION=\"ignore.cgi\" METHOD=\"POST\">"
		echo "<input name=\"form_action\" value=\"del\" type=\"hidden\">"
		echo "<input name=\"form_node\" value=\"$1\" type=\"hidden\">"
		echo "<button onclick=\"document.forms.form_node_del_"$C".submit()\" name=\"form_btn_del\" title=\"Knoten l&ouml;schen\" type=\"button\"><img src="/images/loeschen.gif" align=bottom width=16 height=16 hspace=4></button></FORM></td></tr>"
		if [ $T = 1 ]; then T=2 ;else T=1; fi
		C=$(($C+1))
	fi
}
config_load ddmesh
config_list_foreach ignore_nodes node print_node

cat<<EOM
<tr><td colspan="3"><form name="form_node_del_all" action="ignore.cgi" method="post">
<input name="form_action" value="delall" type="hidden">
<button onclick="document.forms.form_node_del_all.submit()" name="form_btn_delall" title="L&ouml;sche alle Knoten" type="button">Alle Knoten l&ouml;schen</button>
</form></td></tr>

</table>
</fieldset>
<br>
<fieldset class="bubble">
<legend>Knoten hinzuf&uuml;gen</legend>
<form name="form_node_new" action="ignore.cgi" method="post">
<input name="form_action" value="add" type="hidden">
<table>
 <tr><td><input name="form_node" type="text" value="" size="17" maxlength="17">
 <input title="Knoten hinzuf&uuml;gen" type="submit" value="Neu">
</td></tr>
</table>
</form>
</fieldset>
EOM
#end display_ignored_nodes
}

if [ -n "$QUERY_STRING" ]; then
	if [ -n "$form_action" ]; then
		case $form_action in
		  add)
			if [ -z "$(uci get ddmesh.ignore_nodes)" ]; then
				uci add ddmesh ignore_nodes
				uci rename ddmesh.@ignore_nodes[-1]='ignore_nodes'
			fi

			node=$(uhttpd -d $form_node)
			uci
			uci add_list ddmesh.ignore_nodes.node="$node"
			uci_commit.sh
			notebox "Knoten <b>$node</b> wurde hinzugef&uuml;gt. <a href="reset.cgi">Neustart</a> notwendig."
			;;
		  del)
			node=$(uhttpd -d $form_node)
			uci del_list ddmesh.ignore_nodes.node="$node"
			uci_commit.sh
			notebox "Knoten <b>$node</b> wurde gel&ouml;scht. <a href="reset.cgi">Neustart</a> notwendig."
			;;
		  delall)
			uci delete ddmesh.ignore_nodes.node
			uci_commit.sh
			notebox "Alle Knoten wurden gel&ouml;scht. <a href="reset.cgi">Neustart</a> notwendig."
			;;
		esac
	fi
fi

display_ignored_nodes

. /usr/lib/www/page-post.sh ${0%/*}
