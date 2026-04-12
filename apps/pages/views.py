from django.shortcuts import render
from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):
    """Vista para a página de Política de Privacidade (RGPD)"""
    template_name = 'pages/privacy_policy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Política de Privacidade'
        return context


class TermsOfUseView(TemplateView):
    """Vista para a página de Termos de Utilização"""
    template_name = 'pages/terms_of_use.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Termos de Utilização'
        return context


class CookiesPolicyView(TemplateView):
    """Vista para a página de Política de Cookies"""
    template_name = 'pages/cookies_policy.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Política de Cookies'
        return context
