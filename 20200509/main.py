import scanpy as sc
import os
import sys
import argparse
from collections import Counter

sys.path.append("../")
from core.core import Model
from core.ScanpyConfig import *
from core.Config import get_args
from core.detectDoublet import DoubletModule

if __name__=="__main__":
    args=get_args()
    sc.settings.n_jobs=args.n_jobs

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    net=Model(args.path)
    print(net)
    adata=net._load_data()
    print(adata.shape)
    adata=net._subset(adata,[8,11,17],invert=True)
    print(adata.shape)

    metadata=adata.obs
    idents=metadata.idents
    status=["AA" if int(ident) in list(range(1,9)) else "YA" for ident in idents.values]
    print(Counter(status))
    adata.obs["status"]=status

    adata=net._process(adata,"status")
    #adata=net._process(adata)
    adata=net._reduction(adata)
    adata=net._FindMarkers(adata)
    
    print("### Save")
    adata.write(os.path.join(args.outdir,'adata.h5ad'), compression='gzip')
