# A One-Dimensional Generative Diffusion Model for Network Traffic Dataset Generation
This is the source-code of "A One-Dimensional Generative Diffusion Model for Network Traffic Dataset Generation" paper published in "Lecture notes in Computer Science"
## Abstract
Generative AI emerged as a powerful method for generating new data, which is famous for image, video, and text generation. For this inspiration, our study aims to leverage the Generative AI for Network Traffic Dataset Generation. This type of data is very important to cybersecurity, as it is used for detection, prediction, and classification tasks in the network traffic. Recent studies have utilized the variant of Generative AI models for generating Network Traffic Data, gaining considerable achievements. In our study, we proposed a novel approach using the One-Dimensional Generative Diffusion Model to generate the synthetic Network Traffic data. As a result, our proposed model surpasses the previous studies’ models on the UNSW-NB15 dataset, with the Chi-Squared Test and Kolmogorov-Smirnov Test values being 0.863 and 0.838 respectively. Moreover, our proposed method considerably improves the performance of detecting attack activities of network traffic in terms of accuracy and F1-score, demonstrating its powers in cybersecurity.

## Windows

### Run AI

Install uv at <https://github.com/astral-sh/uv>

```pwsh
cd ai
uv venv
.venv/bin/activate.ps1
uv sync
flask --app main run
```

### Run FE

Install bun at <https://bun.sh/docs/installation>

```pwsh
cd fe
bun dev
```

![alt text](resources/image.png)
![alt text](resources/image-1.png)
![alt text](resources/image-2.png)
![alt text](resources/image-3.png)
![alt text](resources/image-4.png)


## Paper citation 
~~~
@inproceedings{viet2024one,
  title={A One-Dimensional Generative Diffusion Model for Network Traffic Dataset Generation},
  author={Viet, Hung Le and Minh, Khoa Tran Dinh and Quang, Nhut Pham and Cong, Danh Nguyen},
  booktitle={International Conference on Computational Data and Social Networks},
  pages={98--109},
  year={2024},
  organization={Springer}
}
~~~
