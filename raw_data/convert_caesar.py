#!/usr/bin/env python
# coding: utf-8

# In[12]:


from scipy.io import loadmat
import meshplot as mp
import numpy as np
from pathlib import Path
import open3d as o3d #install with conda
from tqdm import tqdm
from multiprocessing import Pool


# In[13]:


data_ids = loadmat('VertexIdxSpecParts.mat')
hands = data_ids['idxHand']-1
data = loadmat('faceShapeModel.mat')
f = data['faces'] - 1
not_hands = [i for i in range(f.max()+1) if i not in hands]
mask = np.all(np.isin(f,not_hands),axis=1)
f = f[mask]
source_folder = Path('caesar-fitted-meshes')
target_folder = Path('../dataset/scans/')


# In[14]:


def convert(source_path):
    #print(source_path)
    if not source_path.suffix == '.mat': 
        return
    #print(source_path)
    filename = source_path.relative_to(source_folder)
    target_subfolder = target_folder / filename.with_suffix('')
    target_subfolder = target_subfolder.absolute()
    #print(target_subfolder)
    target_subfolder.mkdir(parents=False, exist_ok=True)

    data = loadmat(source_path)
    v = data['points'] / 1000
    vmesh = o3d.utility.Vector3dVector(v)
    fmesh = o3d.utility.Vector3iVector(f)
    mesh = o3d.geometry.TriangleMesh(vmesh,fmesh)
    mesh = mesh.compute_vertex_normals()
    
    cluster_idx, cluster_size, _ = [np.asarray(x) for x in mesh.cluster_connected_triangles()]
    tri_mask = cluster_idx != np.argmax(cluster_size)
    mesh.remove_triangles_by_mask(tri_mask)
    
    o3dCloud = mesh.sample_points_poisson_disk(20000)
    
    cloudv = np.asarray(o3dCloud.points)
    cloudn = np.asarray(o3dCloud.normals)
    cloudc = np.hstack([cloudv,cloudn])
    
    np.savetxt(str(target_subfolder/filename.with_suffix('.xyz')), cloudc, delimiter=' ',
              fmt='%f')
    #mp.plot(cloudc[:,:3])
    #mp.plot(v,f)
    #break


# In[11]:


pathlist = list(source_folder.iterdir())

with Pool(processes=20) as p:
    with tqdm(total=len(pathlist)) as pbar:
        for i, _ in enumerate(p.imap_unordered(convert, pathlist)):
            pbar.update()
#for source_path in tqdm(list(source_folder.iterdir())):
    


# In[ ]:





# In[ ]:




