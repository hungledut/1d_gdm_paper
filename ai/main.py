#%%
import pandas as pd
import numpy as np
import category_encoders as ce
import torch
from sklearn.preprocessing import MinMaxScaler
from denoising_diffusion_pytorch import Unet1D, GaussianDiffusion1D, Trainer1D, Dataset1D
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import threading
import time


app = Flask(__name__)
CORS(app, support_credentials=True)


diffusion = None
trainer = None
scaler = None
encoder = None
data_cols = None
res_cached = []

infer_mutex = threading.Lock()

@app.route('/run')
@cross_origin(supports_credentials=True)
def run():
    global res_cached
    count = int(request.args.get('count', 10))
    res = [] 
    if len(res_cached) > count:
        res = res_cached[:count]
        res_cached = res_cached[count:]
        time.sleep(3)
    else:
        with infer_mutex:
            res = res_cached[:count]
            res_cached = res_cached[count:]
    return jsonify(res)


def load_model(input, weights):
    global trainer
    global diffusion
    global scaler
    global encoder
    global data_cols
    data = pd.read_csv(input)
    data = data.drop(columns = 'id')
    #Create object for one-hot encoding
    encoder=ce.OneHotEncoder(cols=['state','proto','attack_cat','service'],handle_unknown='return_nan',return_df=True,use_cat_names=True)
    #Fit and transform Data
    data_encoded = encoder.fit_transform(data)
    scaler = MinMaxScaler()
    dataset1_norm = scaler.fit_transform(data_encoded.values)
    dataset1 = torch.Tensor(dataset1_norm)
    dataset1 = torch.unsqueeze(dataset1,1)
    shape0 = dataset1.shape[0]
    shape1 = dataset1.shape[1]
    dataset1 = torch.concat([dataset1,torch.zeros(shape0,shape1,3)],dim=2)
    data_cols = data_encoded.columns
    ######################################################################################


    model = Unet1D(
        dim = 16,
        dim_mults = (1, 2, 4, 8),
        channels = 1
        )

    diffusion = GaussianDiffusion1D(
        model,
        seq_length = 208,
        timesteps = 1000,
        objective = 'pred_v'
        )

    dataset = Dataset1D(dataset1)  
    amp = False if not torch.cuda.is_available() else True

    trainer = Trainer1D(
        diffusion,
        dataset = dataset,
        train_batch_size = 1,
        train_lr = 8e-5,
        train_num_steps = 10000,         # total training steps
        gradient_accumulate_every = 2,    # gradient accumulation steps
        ema_decay = 0.995,                # exponential moving average decay
        amp = amp,                       # turn on mixed precision
        )
    trainer.load(weights)


def infer(count: int = 100):
    # Acquire mutex before running inference
    with infer_mutex:
        if diffusion is None:
            load_model()
        sampled_seq = diffusion.sample(batch_size = count)
        sampled_seq_sq = torch.squeeze(sampled_seq, 1)[:,0:-3]
        print(f"{sampled_seq_sq.shape=}")
        sampled_seq_sq = scaler.inverse_transform(sampled_seq_sq.cpu())
        a = sampled_seq_sq
        #### 
        argmax = np.argmax(a[:,1:134],axis=1) + 1
        for i in range(0,a.shape[0]):
            for j in range(0,a.shape[1]):
                if j == argmax[i] and j >= 1 and j <= 133:
                    a[i][j] = 1
                elif j != argmax[i] and j >= 1 and j <= 133:
                    a[i][j] = 0
        ###
        argmax = np.argmax(a[:,134:147],axis=1) + 134
        for i in range(0,a.shape[0]):
            for j in range(0,a.shape[1]):
                if j == argmax[i] and j >= 134 and j <= 146:
                    a[i][j] = 1
                elif j != argmax[i] and j >= 134 and j <= 146:
                    a[i][j] = 0
        ###
        argmax = np.argmax(a[:,147:156],axis=1) + 147
        for i in range(0,a.shape[0]):
            for j in range(0,a.shape[1]):
                if j == argmax[i] and j >= 147 and j <= 155:
                    a[i][j] = 1
                elif j != argmax[i] and j >= 147 and j <= 155:
                    a[i][j] = 0
        ###
        argmax = np.argmax(a[:,194:204],axis=1) + 194
        for i in range(0,a.shape[0]):
            for j in range(0,a.shape[1]):
                if j == argmax[i] and j >= 194 and j <= 203:
                    a[i][j] = 1
                elif j != argmax[i] and j >= 194 and j <= 203:
                    a[i][j] = 0
        sampled_seq_df = pd.DataFrame(a)
        sampled_seq_df.columns = data_cols
        data_decoded = encoder.inverse_transform(sampled_seq_df)
        columns_to_convert = ['spkts', 'dpkts', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'swin', 'stcpb', 'dtcpb', 'dwin', 'smean', 'dmean', 'trans_depth',
                         'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login',
                          'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports', 'label']

        data_decoded[columns_to_convert] = data_decoded[columns_to_convert].astype(float).round().astype(int)

        return data_decoded.to_dict(orient='records')


#%%
input = 'UNSW_NB15_testing-set.csv'
weights = 'network-traffic'
load_model(input, weights)


#%%
def add_res_to_cache():
    global res_cached
    while True:
        if len(res_cached) < 10000:
            res = infer(1000)
            res_cached.extend(res)
            print(f'Added {len(res_cached)} results to cache')
        time.sleep(1)
t = threading.Thread(target=add_res_to_cache,args=())
t.start()

#%%


