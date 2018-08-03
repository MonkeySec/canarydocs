import tempfile
import shutil
import json
import sys, argparse
from zipfile import ZipFile, ZipInfo
from cStringIO import StringIO

MODE_DIRECTORY = 0x10

#Read all configuration values in from the config.json file
def readConfiguration(configfile):
	print("Using Config: {0}".format(configfile))

	global websvr_host, websvr_port, websvr_uri, template_file, org_name, canary_email_domain
	

	#Read in the configuration file called config.json
	try:
		config = json.loads(open(configfile).read())
	except IOError:
		print("ERROR: Failed to read in the",configfile,"file.")
		sys.exit()

	#Read in config variables
	websvr_host = ', '.join(config['WEB_SVR_DETAILS']['hostname'])
	websvr_port = ', '.join(config['WEB_SVR_DETAILS']['port']) 
	websvr_uri = ', '.join(config['WEB_SVR_DETAILS']['URI_PATH'])
	template_file = ', '.join(config['DOC_INFO']['template_filename'])
	org_name = ', '.join(config['DOC_INFO']['organisation'])
	canary_email_domain = ', '.join(config['DOC_INFO']['canary_email_domain'])

def zipinfo_contents_replace(zipfile=None, zipinfo=None, search1=None, search2=None, replace1=None, replace2=None):
	"""Given an entry in a zip file, extract the file and perform a search
       and replace on the contents. Returns the contents as a string."""
	dirname = tempfile.mkdtemp()
	fname = zipfile.extract(zipinfo, dirname)
	with open(fname, 'r') as fd:
		contents = fd.read().replace(search1, replace1).replace(search2, replace2)
	shutil.rmtree(dirname)
	return contents

def make_canary_msword(url=None, mail=None):
	
	with open(template, 'r') as f:
		input_buf = StringIO(f.read())
	output_buf = StringIO()
	output_zip = ZipFile(output_buf, 'w')

	with ZipFile(input_buf, 'r') as doc:
		for entry in doc.filelist:
			if entry.external_attr & MODE_DIRECTORY:
				continue

			contents = zipinfo_contents_replace(zipfile=doc, zipinfo=entry,search1="REPLACE_EMAIL_HASH_HERE", search2="replace_url_hash_here", replace1=mail, replace2=url)
			output_zip.writestr(entry, contents)
			#contents = zipinfo_contents_replace(zipfile=doc, zipinfo=entry, search="replace_url_hash_here", replace=url)
			#output_zip.writestr(entry, contents2)
	output_zip.close()
	return output_buf.getvalue()

	
#http://REPLACE_DOCWEBSVR_NAME:REPLACE_DOCWEBSVR_PORT/REPLACE_DOCWEBSVR_URIPATH/REPLACE_DOC_URL_HASH
#REPLACE_ORG 
#REPLACE_EMAIL_HASH_HERE
	
#Main() func, reads the configuration file and calls Canary Doc Gen Function
def main(argv):
	configfile = argv[0]
	readConfiguration(configfile)
	
	if arv[1] != '':
		canaryHash = argv[1]
	else:
		canaryHash = raw_input("Please enter the hash of the canary record created: ")
		
	if argv[2] != '':
		canaryFileName = argv[2]
	else:
		canaryFileName = raw_input("Please enter the file name of the canary document to create (contents relate to passwords in template): ")
	
	canaryMail = canaryHash + canary_email_domain

	with open(canaryFileName, 'w+') as f:
		f.write(make_canary_msword(url=canaryHash, mail=canaryMail))

#Run main, use ArgParser to display --help on CLI and allow input of Config File arguemnt
if __name__ == "__main__": 
	parser = argparse.ArgumentParser(description='Optional config file.')
	parser.add_argument('--config',default='config.json', help="Add a config file path")
	parser.add_argument('--canaryhash', default='', help="Specify a unique canary hash record.")
	parser.add_argument('--filename', default='', help="Specify a name for the canary document to be called.")
	inputvar = parser.parse_args()
	main(inputvar)
