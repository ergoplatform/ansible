import sys
import os
from colors import color
from jsonschema.exceptions import RefResolutionError
from openapi_spec_validator import openapi_v3_spec_validator
from openapi_spec_validator.handlers import UrlHandler
from six.moves.urllib.parse import urlparse


def validate(url):
    counter = 0

    try:
        handler = UrlHandler('http', 'https', 'file')

        if not urlparse(url).scheme:
            url = 'file://' + os.path.join(os.getcwd(), url)

        spec = handler(url)

        for i in openapi_v3_spec_validator.iter_errors(spec, spec_url=url):
            counter += 1
            print_error(counter, ':'.join(i.absolute_path), i.message, i.instance)

    except RefResolutionError as e:
        counter += 1
        print_error(counter, '', 'Unable to resolve {} in {}'.format(e.__context__.args[0], e.args[0]), '')

    except BaseException:
        counter += 1
        print_error(counter, '', sys.exc_info()[0], '')

    finally:
        if counter > 0:
            print()
            print(color(' [FAIL] {:d} errors found '.format(counter), fg='white', bg='red', style='bold'))
            return 1
        else:
            print(color(' [PASS] No errors found ', fg='white', bg='green', style='bold'))
            return 0


def print_error(count, path, message, instance):
    print()
    print(color('Error #{:d} in [{}]:'.format(count, path or 'unknown'), style='bold'))
    print("    {}".format(message))
    print("    {}".format(instance))


def help():
    print('usage: ' + os.path.basename(__file__) + ' <spec_url_or_path>')


def main(argv):
    if len(argv) == 0:
        print('Invalid usage!')
        help()
        sys.exit(2)

    sys.exit(validate(argv[0]))


if __name__ == "__main__":
    main(sys.argv[1:])
