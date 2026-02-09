import urllib.request
import json
import os
import mimetypes
import uuid

def test_upload():
    url = "http://localhost:5000/api/upload"
    file_path = "dummy_resume.docx"
    boundary = str(uuid.uuid4())
    
    if not os.path.exists(file_path):
        print("Error: dummy_resume.docx not found. Please create it first.")
        return

    with open(file_path, 'rb') as f:
        file_content = f.read()

    # Construct Multipart Form Data
    data = []
    
    # File Field
    data.append(f'--{boundary}'.encode())
    data.append(f'Content-Disposition: form-data; name="resume"; filename="dummy_resume.docx"'.encode())
    data.append(f'Content-Type: {mimetypes.guess_type(file_path)[0] or "application/octet-stream"}'.encode())
    data.append(b'')
    data.append(file_content)
    
    # Text Field (Job Description)
    data.append(f'--{boundary}'.encode())
    data.append('Content-Disposition: form-data; name="job_description"'.encode())
    data.append(b'')
    data.append('Looking for a Senior Python Developer with experience in Flask, SQL, and Docker.'.encode())
    
    data.append(f'--{boundary}--'.encode())
    data.append(b'')
    
    body = b'\r\n'.join(data)
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body))
    }

    req = urllib.request.Request(url, data=body, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n[SUCCESS] API Response Received:")
            print(json.dumps(result, indent=2))
            
            if result.get("success"):
                print("\n[SUCCESS] Verification Passed: Resume analyzed successfully!")
            else:
                print("\n❌ Verification Failed: API returned success=False")
                
    except urllib.error.HTTPError as e:
        print(f"\n[ERROR] API Request Failed: {e.code} {e.reason}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {e}")

if __name__ == "__main__":
    test_upload()
