import boto
# import boto.ec2
from boto.s3.key import Key

## check what's already online
def main():

	# conn = boto.ec2.connect_to_region("eu-west-1")
	conn   = boto.connect_s3()
	bucket = conn.get_bucket("map-images-jc")

	for k in bucket.list():
		print k, k.key


if __name__ == '__main__':
	main()