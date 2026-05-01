import pandas as pd
import re

def is_valid_email(email):
    # Blacklist of bad extensions or keywords
    bad_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.js', '.css']
    bad_keywords = ['sentry.io', 'wixpress.com', 'w3.org', 'schema.org', 'google.com', 'facebook.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com', 'apple.com', 'microsoft.com', 'amazonaws.com', 'cloudflare.com', 'jquery.com', 'fontawesome.com', 'wp.com', 'wordpress.com']
    
    email = str(email).lower().strip()
    
    if not email:
        return False
        
    if len(email) > 60:
        return False
        
    for ext in bad_extensions:
        if email.endswith(ext):
            return False
            
    for kw in bad_keywords:
        if kw in email:
            return False
            
    # Remove emails with typical hexadecimal blobs (like md5 or uuid)
    if re.search(r'[0-9a-f]{8,}', email):
        return False
        
    # Basic email format check
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return False
        
    return True

def rank_email(email):
    # Lower rank is better
    email = email.lower()
    if 'contacto' in email or 'contact' in email:
        return 1
    if 'ventas' in email or 'sales' in email or 'comercial' in email:
        return 2
    if 'info' in email or 'hola' in email or 'hello' in email:
        return 3
    if 'gerencia' in email or 'gerente' in email or 'director' in email:
        return 4
    if 'admin' in email:
        return 5
    return 10

def clean_row(row):
    scraped = str(row.get('Email_Scrapeado', ''))
    original = str(row.get('Email', ''))
    
    candidates = set()
    if pd.notna(scraped) and scraped and scraped.lower() not in ['nan', 'none']:
        for e in scraped.split(' | '):
            candidates.add(e.strip())
            
    if pd.notna(original) and original and original.lower() not in ['nan', 'none', 'no encontrado', '']:
        for e in re.split(r'[,;|\s]+', original):
            candidates.add(e.strip())
            
    valid_emails = [e for e in candidates if is_valid_email(e)]
    valid_emails.sort(key=lambda x: (rank_email(x), x))
    
    return valid_emails

def main():
    print("Leyendo Exponor_Emails_Scrapeados.xlsx...")
    df = pd.read_excel('Exponor_Emails_Scrapeados.xlsx')
    
    print("Limpiando emails y separando en columnas...")
    df['Lista_Emails'] = df.apply(clean_row, axis=1)
    
    max_emails = df['Lista_Emails'].apply(len).max()
    
    # Crear las nuevas columnas
    for i in range(max_emails):
        df[f'Email_{i+1}'] = df['Lista_Emails'].apply(lambda x: x[i] if i < len(x) else '')
    
    # Eliminar columnas temporales y antiguas para dejarlo ultra limpio
    cols_to_drop = ['Lista_Emails', 'Email', 'Email_Scrapeado', 'Email_Final']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    output_file = 'Exponor_Emails_Limpios.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Limpieza completa. Archivo guardado como {output_file} con {max_emails} columnas máximas de email.")
    
    # Show a sample
    email_cols = [f'Email_{i+1}' for i in range(max_emails)]
    print("\nMuestra de los emails finales separados en columnas:")
    print(df[['Empresa'] + email_cols].dropna(subset=['Email_1']).head(15).to_string())

if __name__ == '__main__':
    main()
