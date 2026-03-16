import unittest
import importlib.util
import sys
import json
import os

# Import convert-to-astro.py as a module
spec = importlib.util.spec_from_file_location("convert_to_astro", "./convert-to-astro.py")
convert_to_astro = importlib.util.module_from_spec(spec)
sys.modules["convert_to_astro"] = convert_to_astro
spec.loader.exec_module(convert_to_astro)

class TestExtractMeta(unittest.TestCase):

    def test_extract_meta_valid_jsonld(self):
        """Test extraction of valid JSON-LD schema."""
        html = '''
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description">
                <link rel="canonical" href="https://example.com/test">
                <script type="application/ld+json">
                {
                    "@context": "https://schema.org",
                    "@type": "Article",
                    "headline": "Test Article"
                }
                </script>
            </head>
            <body></body>
        </html>
        '''
        title, description, canonical, schema = convert_to_astro.extract_meta(html)

        self.assertEqual(title, "Test Page")
        self.assertEqual(description, "Test description")
        self.assertEqual(canonical, "https://example.com/test")
        self.assertEqual(schema, {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "Test Article"
        })

    def test_extract_meta_invalid_jsonld(self):
        """Test extraction when JSON-LD is invalid, it should safely return None for schema."""
        html = '''
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description">
                <link rel="canonical" href="https://example.com/test">
                <script type="application/ld+json">
                {
                    "@context": "https://schema.org",
                    "@type": "Article",
                    "headline": "Test Article",
                    invalid json string
                }
                </script>
            </head>
            <body></body>
        </html>
        '''
        title, description, canonical, schema = convert_to_astro.extract_meta(html)

        self.assertEqual(title, "Test Page")
        self.assertEqual(description, "Test description")
        self.assertEqual(canonical, "https://example.com/test")
        self.assertIsNone(schema)

    def test_extract_meta_missing_jsonld(self):
        """Test extraction when JSON-LD is missing, schema should be None."""
        html = '''
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description">
                <link rel="canonical" href="https://example.com/test">
            </head>
            <body></body>
        </html>
        '''
        title, description, canonical, schema = convert_to_astro.extract_meta(html)

        self.assertEqual(title, "Test Page")
        self.assertEqual(description, "Test description")
        self.assertEqual(canonical, "https://example.com/test")
        self.assertIsNone(schema)

    def test_extract_meta_missing_meta(self):
        """Test extraction when meta tags and title are missing."""
        html = '''
        <html>
            <head>
            </head>
            <body></body>
        </html>
        '''
        title, description, canonical, schema = convert_to_astro.extract_meta(html)

        self.assertEqual(title, "Untitled")
        self.assertEqual(description, "")
        self.assertEqual(canonical, "")
        self.assertIsNone(schema)

    def test_extract_meta_alternate_description(self):
        """Test extraction of alternate description tag format."""
        html = '''
        <html>
            <head>
                <title>Test Page</title>
                <meta content="Test description" name="description">
            </head>
            <body></body>
        </html>
        '''
        title, description, canonical, schema = convert_to_astro.extract_meta(html)

        self.assertEqual(description, "Test description")

if __name__ == '__main__':
    unittest.main()
