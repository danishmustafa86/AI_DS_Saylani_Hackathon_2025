#!/usr/bin/env python3
"""
Environment Setup Helper Script
Helps you create your .env file from the template
"""
import os
import secrets
import shutil

def generate_secret_key():
    """Generate a secure random key"""
    return secrets.token_urlsafe(32)

def setup_env():
    """Interactive setup for .env file"""
    print("🚀 AI Campus Admin Agent - Environment Setup")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("❌ Setup cancelled.")
            return
    
    # Copy template
    if os.path.exists('env.example'):
        shutil.copy('env.example', '.env')
        print("✅ Created .env file from template")
    else:
        print("❌ env.example file not found!")
        return
    
    print("\n📝 Let's configure your environment variables:")
    print("   (Press Enter to keep default values)")
    
    # Generate secure keys
    secret_key = generate_secret_key()
    jwt_secret = generate_secret_key()
    
    # Interactive configuration
    configs = {}
    
    print(f"\n🔐 Security Keys:")
    configs['SECRET_KEY'] = input(f"Secret Key [{secret_key[:20]}...]: ") or secret_key
    configs['JWT_SECRET_KEY'] = input(f"JWT Secret Key [{jwt_secret[:20]}...]: ") or jwt_secret
    
    print(f"\n🤖 AI Services:")
    configs['OPENAI_API_KEY'] = input("OpenAI API Key (required): ")
    configs['ELEVENLABS_API_KEY'] = input("ElevenLabs API Key (optional): ") or ""
    
    print(f"\n🗄️  Database:")
    configs['MONGODB_URI'] = input("MongoDB URI [mongodb://localhost:27017]: ") or "mongodb://localhost:27017"
    configs['MONGODB_DB'] = input("Database Name [ai_campus]: ") or "ai_campus"
    
    print(f"\n📧 Email (optional):")
    configs['SMTP_USERNAME'] = input("Email Username: ") or ""
    configs['SMTP_PASSWORD'] = input("Email Password: ") or ""
    
    # Update .env file
    with open('.env', 'r') as f:
        content = f.read()
    
    for key, value in configs.items():
        if value:  # Only replace if value is provided
            # Find and replace the placeholder
            placeholder = f"{key}=your-"
            if placeholder in content:
                content = content.replace(f"{key}=your-{key.lower().replace('_', '-')}-here", f"{key}={value}")
                content = content.replace(f"{key}=your-{key.lower().replace('_', '-')}-change-this-in-production", f"{key}={value}")
                content = content.replace(f"{key}=your-{key.lower().replace('_', '-')}-change-this-to-something-secure", f"{key}={value}")
            else:
                # Direct replacement
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith(f"{key}="):
                        lines[i] = f"{key}={value}"
                        break
                content = '\n'.join(lines)
    
    # Write updated content
    with open('.env', 'w') as f:
        f.write(content)
    
    print("\n✅ Environment configuration complete!")
    print("\n📋 Next steps:")
    print("   1. Review your .env file")
    print("   2. Make sure MongoDB is running")
    print("   3. Install dependencies: poetry install")
    print("   4. Start the backend: poetry run python main.py")
    
    if not configs['OPENAI_API_KEY']:
        print("\n⚠️  Warning: No OpenAI API key provided.")
        print("   Get one from: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    setup_env()
