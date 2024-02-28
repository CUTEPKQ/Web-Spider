<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="image/spider.jpg" alt="Logo" width="280" height="180">
  </a>
  <h3 align="center">Weibo_Spider</h3>
  <p align="center">
    ^_^对微博话题内容进行爬取^_^
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

本项目利用python对微博话题进行爬取，同时利用FastAPI进行API的搭建。
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

首先安装环境依赖库，对于FastAPI,推荐安装所有的可选依赖及对应功能
* BeautifulSoup
  ```sh
  pip install beautifulsoup4
  ```
* FastAPI
  ```sh
  pip install "fastapi[all]"
  ```

### Installation


Clone the repo
   ```sh
   git clone https://github.com/CUTEPKQ/Web-Spider.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
1. 在*config.json*文件中
   * 将weibo_cookies更换为自己的cookies
   * query修改为要查询的话题
   * page 代表要爬取的页数（一页十条数据）
2. 运行
   * 直接运行*main.py*文件，可以得到爬取的数据（评论内容、评论时间），并将其保存为csv文件
3. API服务
   * 运行*api.py*文件，启用api服务（默认host为localhost,端口号为9394，使用前请**确保该端口未被占用**）
   * 运行*api_test.py*文件，验证api
  




<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* 参考博客(https://blog.csdn.net/m0_72947390/article/details/132832280)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

