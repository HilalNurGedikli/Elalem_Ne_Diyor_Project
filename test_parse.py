#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test file for parse_gemini_analysis function
import sys
sys.path.append('services')

from gemini_utils import parse_gemini_analysis, format_analysis_for_ui

# Test metni
test_text = """İşte Trendyol hakkında, kullanıcı yorumlarına dayalı değerlendirme:

**Güvenilirlik:** ETBIS kayıtlıdır ve kurumsal bir yapıya sahip, ancak yoğun şikayetler güven algısını zayıflatmaktadır.
**Genel Kullanıcı Memnuniyeti:** Pazarlama başarısı yüksek olsa da, operasyonel sorunlar ve yetersiz müşteri hizmeti genel memnuniyeti düşürmektedir.
**Mağazanın sevilen yönleri:** Geniş ürün yelpazesi, cazip kampanyalar, trendleri yakalaması ve başarılı influencer pazarlamasıdır.
**Mağazanın sevilmeyen yönleri:** Müşteri hizmetlerine ulaşım zorluğu, iade sorunları, yanlış/eksik ürün ve yanıltıcı kampanya yönetimidir.
**En çok memnun olunan konular:** Geniş ürün yelpazesi, güncel trend ürünler ve cazip indirim fırsatları sunmasıdır.
**Kronik problemleri:** Müşteri hizmeti yetersizliği, iade/değişim süreçlerindeki aksaklıklar ve ürün teslimat/kalite sorunlarıdır.
**Puanlama:** 5/10
**Alışveriş yapılmasını tavsiye eder misin:** Şikayetler göz önüne alındığında dikkatli olunmalı; potansiyel riskleri kabul edenler için cazip olabilir.
**Genel gemini yorumu:** Pazarlama gücüne rağmen, operasyonel zayıflıkları ve müşteri hizmeti sorunları kullanıcı deneyimini olumsuz etkileyen büyük bir platformdur."""

print("🔍 Testing parse_gemini_analysis function...")
print("=" * 50)

# Parse et
parsed = parse_gemini_analysis(test_text)

print("\n📊 PARSED RESULTS:")
for key, value in parsed.items():
    print(f"   {key}: {value}")

print("\n🎨 FORMATTED FOR UI:")
formatted = format_analysis_for_ui(parsed)

for section in formatted['sections']:
    print(f"   {section['title']}: {section['content']}")

print(f"\nRating: {formatted['summary']['rating']}")
print(f"Recommendation: {formatted['summary']['recommendation']}")
