# How to install and run Fooocue on AWS SageMaker Studio Lab

## What is AWS SageMaker Studio Lab

AWS SageMaker Studio Lab is a variation of SageMaker Studio designed for educational purposes and cost-effective learning. It provides a similar integrated environment but is tailored for individual users, researchers, and educators who want to experiment with machine learning concepts without incurring the costs associated with a full SageMaker Studio environment.

Some key features of SageMaker Studio Lab include:

- **Jupyter Notebooks:** It allows users to create and run Jupyter notebooks for interactive development and exploration.
- **Pre-configured Environments:** SageMaker Studio Lab comes with pre-configured environments for popular machine learning frameworks, making it easier for users to get started.
- **Cost Management:** SageMaker Studio Lab is designed to be more cost-effective for individual users, making it suitable for learning and experimentation.
- **Collaboration:** It supports collaboration among users, making it a useful tool for educational settings where multiple users may work on machine learning projects together.

## What is Fooocus

Fooocus is an image generating software based on Gradio. Fooocus is a rethinking of Stable Diffusion and Midjourney’s designs:

- Learned from Stable Diffusion, the software is offline, open source, and free.
- Learned from Midjourney, the manual tweaking is not needed, and users only need to focus on the prompts and images.

Fooocus has included and automated lots of inner optimizations and quality improvements. Users can forget all those difficult technical parameters, and just enjoy the interaction between human and computer to "explore new mediums of thought and expanding the imaginative powers of the human species".

Fooocus has simplified the installation. Between pressing "download" and generating the first image, the number of needed mouse clicks is strictly limited to less than 3. Minimal GPU memory requirement is 4GB (Nvidia). Here's the official GitHub repo for Fooocus: https://github.com/lllyasviel/Fooocus

## About AWS SageMaker Studio Lab and Fooocus

So far the official implementation of Fooocus has been done on local systems and Google Colab. AWS SageMaker Studio Lab is another alternative to Google Colab, it even has its own official notebook to create text2image content using Stable Diffussion. Here's how you can run Fooocus on AWS SageMaker Studio Lab:

1. Request for a free SageMaker account from the following link: https://studiolab.sagemaker.aws/
2. Once your request has been approved, create a new account using the link they have sent in their email
3. Log in to your account
4. Once logged in, create a new runtime with a GPU from My Projects and then click Open Project
5. Add this repository once the Jupyter Lab opens: https://github.com/rajtilakjee/fooocus-sagemaker-studio.git
6. Open a terminal on SageMaker and run the following command: `sh start.sh`
7. On a new browser tab, register for a free account on ngrok and copy the Authtoken: https://ngrok.com/
8. Paste the Authtoken in the SageMaker terminal when asked
9. Now copy the domain from ngrok and enter in the SageMaker terminal
10. Once you get the message on the terminal that the app was started, paste this same domain in a new browser tab and start using Fooocus!

If you find this tutorial and repo helpful do give it a star. If you can, do donate through GitHub so that I can work on the other projects here. Thank you!
