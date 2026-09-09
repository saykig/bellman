"""Candidate reduction warrants reuse both established candidate producers."""
from reduction import verify_map,restrict,digest
# valuation_producer imports the older incentive producer under its own name.
from valuation_producer import produce as consistency_produce


def produce(source,target,q,w,epsilon='0'):
    verify_map(source,target,q)
    return {'schema':'bellman.public-tag-erasure-warrant.v1','source_sha256':digest(source),
            'target_sha256':digest(target),'reduction':q,
            'source_warrant':consistency_produce(source,w,epsilon),
            'target_warrant':consistency_produce(target,restrict(w,q),epsilon)}
