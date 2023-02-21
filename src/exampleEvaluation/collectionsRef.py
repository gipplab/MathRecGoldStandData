import sys
import elasticsearch
import elasticsearch.helpers
import gzip
import marshal


def all_items(dumpfile):
    while True:
        try:
            yield marshal.load(dumpfile)
        except EOFError:
            break


es = elasticsearch.Elasticsearch(['localhost:9200'], timeout=120)
with gzip.open(sys.argv[1], 'rb') as dumpfile:
    prefix = marshal.load(dumpfile)
    print(f'{prefix}*')
    # es.indices.delete(f'{prefix}*')
    specs = marshal.load(dumpfile)
    for spec in specs:
        # print(spec)
        # sys.exit(0)
        es.indices.create(spec['fullname'], body=spec['settings'])
        es.indices.put_mapping(index=spec['fullname'], body=spec['mapping'])
        es.indices.put_alias(index=spec['fullname'], name=spec['alias'])
        break
    for _ in elasticsearch.helpers.parallel_bulk(es, all_items(dumpfile)):
        pass
    es.indices.refresh(index= f'{prefix}*', request_timeout=240)