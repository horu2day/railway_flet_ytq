import os

def create_directory_structure():
    # 프로젝트 루트 디렉토리
    root_dir = "flet_ytq"
    
    # 디렉토리 구조
    directories = [
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/utils",
        "frontend/public",
        "backend/api/routes",
        "backend/auth",
        "backend/config",
        "backend/utils"
    ]
    
    # 파일 구조
    files = {
        "frontend/src/pages/main.py": "",
        "frontend/src/app.py": "",
        "frontend/requirements.txt": """flet==0.25.2
flet-core==0.25.2
httpx==0.27.2
pillow==11.0.0""",
        "backend/api/routes/auth_routes.py": "",
        "backend/api/routes/youtube_routes.py": "",
        "backend/auth/authapp.py": "",
        "backend/auth/authmanager.py": "",
        "backend/auth/client_secrets.json": "{}",
        "backend/config/config.json": "{}",
        "backend/requirements.txt": """fastapi==0.115.6
uvicorn==0.34.0
google-auth==2.37.0
google-auth-oauthlib==1.2.1
google-generativeai==0.8.3
supabase==2.10.0
python-jose==3.3.0
python-multipart==0.0.6
youtube-transcript-api==0.6.3""",
        "README.md": "# Flet YouTube Query (YTQ) Application"
    }
    
    # 디렉토리 생성
    for directory in directories:
        full_path = os.path.join(root_dir, directory)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created directory: {full_path}")
    
    # 파일 생성
    for file_path, content in files.items():
        full_path = os.path.join(root_dir, file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {full_path}")

if __name__ == "__main__":
    create_directory_structure()
    print("\nProject structure created successfully!")