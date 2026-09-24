# ==========================================
# Stage 1: Build & Dependencies
# ==========================================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# ساخت virtualenv و نصب پکیج‌ها در محیط مجزا
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# کپی requirements و نصب بهینه
COPY src/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Minimal Production Runner
# ==========================================
FROM python:3.12-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# ساخت کاربر غیر root برای پاس کردن استانداردهای امنیتی
RUN groupadd -r appgroup && useradd -r -g appgroup -s /bin/false appuser

# انتقال پکیج‌های نصب‌شده از استیج اول
COPY --from=builder /opt/venv /opt/venv

# کپی فایل‌های برنامه و قالب HTML در مسیر مناسب
COPY src/ /app/
COPY templates/ /app/templates/

# تغییر دسترسی به کاربر محدود
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]