# Deploying the Alaska Department of Snow Chatbot to Google Cloud Run

This guide provides step-by-step instructions for deploying the Alaska Department of Snow Chatbot to Google Cloud Run.

## Why Google Cloud Run?

Google Cloud Run is an ideal platform for deploying the Alaska Department of Snow Chatbot for several reasons:

1. **Serverless Architecture**: Cloud Run is a fully managed serverless platform that automatically scales based on traffic, from zero to any number of containers as needed. This means you only pay for the resources you use, making it cost-effective for applications with variable traffic patterns.

2. **Container-based Deployment**: Cloud Run allows you to deploy containerized applications without managing the underlying infrastructure, providing flexibility while reducing operational overhead.

3. **Integration with Google Cloud Services**: Since our chatbot uses Google Cloud services like BigQuery for vector search and Vertex AI/Gemini for LLM capabilities, deploying on Cloud Run provides seamless integration and optimal performance.

4. **Automatic Scaling**: The chatbot can handle varying loads efficiently as Cloud Run automatically scales up during peak usage and scales down to zero when there's no traffic, optimizing resource usage and costs.

5. **Security**: Cloud Run integrates with Google Cloud's IAM and Secret Manager, making it easy to manage service accounts and sensitive credentials securely.

6. **Global Reach**: Cloud Run can be deployed in multiple regions, ensuring low-latency access for users across different geographical locations.

7. **HTTPS by Default**: Cloud Run provides automatic HTTPS, ensuring secure communication between users and the chatbot.

## Prerequisites

1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured
2. [Docker](https://docs.docker.com/get-docker/) installed
3. A Google Cloud project with billing enabled
4. Service account with necessary permissions for:
   - Cloud Run
   - Artifact Registry
   - BigQuery
   - Vertex AI / Gemini API

## Step 1: Set up environment variables

```bash
# Set your Google Cloud project ID
export PROJECT_ID="your-project-id"
export REGION="us-central1"  # Choose an appropriate region
```

## Step 2: Build the Docker image

```bash
# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/ads-chatbot .
```

## Step 3: Configure authentication

The application needs to authenticate with Google Cloud services. For Cloud Run, you have two options:

### Option 1: Use a service account key (development/testing)

1. Create a service account with the necessary permissions:
   - BigQuery User
   - BigQuery Data Viewer
   - Vertex AI User

2. Create and download a service account key:
   ```bash
   gcloud iam service-accounts keys create key.json \
     --iam-account=SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
   ```

3. When deploying to Cloud Run, you'll provide this key as a secret.

### Option 2: Use workload identity (recommended for production)

Cloud Run can use the service account assigned to it for authentication, which is more secure than using a key file.

## Step 4: Push the Docker image to Google Container Registry

```bash
# Configure Docker to use gcloud as a credential helper
gcloud auth configure-docker

# Push the image to Google Container Registry
docker push gcr.io/$PROJECT_ID/ads-chatbot
```

## Step 5: Deploy to Google Cloud Run

```bash
# Deploy the container to Cloud Run
gcloud run deploy ads-chatbot \
  --image gcr.io/$PROJECT_ID/ads-chatbot \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --service-account SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
```

If you're using a service account key, you'll need to create a secret and mount it:

```bash
# Create a secret with your service account key
gcloud secrets create ads-chatbot-sa-key --data-file=key.json

# Deploy with the secret mounted
gcloud run deploy ads-chatbot \
  --image gcr.io/$PROJECT_ID/ads-chatbot \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --service-account SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com \
  --set-secrets=GOOGLE_APPLICATION_CREDENTIALS=/secrets/key.json:ads-chatbot-sa-key:latest \
  --update-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID
```

## Step 6: Access your deployed chatbot

After deployment, Cloud Run will provide a URL where your chatbot is accessible. You can find this URL in the Cloud Run console or from the output of the deployment command.

## Troubleshooting

1. **Authentication issues**: Ensure your service account has the necessary permissions.
2. **Container crashes**: Check the Cloud Run logs for error messages.
3. **BigQuery errors**: Verify that your BigQuery dataset and tables exist and are accessible.
4. **Gemini API errors**: Ensure the Gemini API is enabled in your project and your service account has access.

## Additional Configuration

### Scaling

Cloud Run automatically scales based on traffic. You can configure minimum and maximum instances:

```bash
gcloud run services update ads-chatbot \
  --min-instances=1 \
  --max-instances=10
```

### Memory and CPU

Adjust resources as needed:

```bash
gcloud run services update ads-chatbot \
  --memory=2Gi \
  --cpu=2
```

### Environment Variables

You can set additional environment variables:

```bash
gcloud run services update ads-chatbot \
  --update-env-vars MODEL="gemini-2.0-flash-001"
```
