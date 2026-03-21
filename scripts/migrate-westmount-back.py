#!/usr/bin/env python3
"""
Migrate westmount-fundamentals repo back into photonbuilder monorepo.
Zero URL changes. Refactors during import to avoid post-merge cleanup.

What it does:
1. Copies 36 unique pages (fixes import paths)
2. Copies dynamic routes + templates + types
3. Copies all data files (IV, prospect, registry, cross-links, etc.)
4. Deletes static IV pages replaced by dynamic route
5. Standardizes meta fields (section → category)
6. Copies scripts
7. Reports what changed
"""

import os
import re
import shutil
import json
from pathlib import Path

WM = Path(os.path.expanduser("~/Desktop/westmount-fundamentals"))
PB = Path(os.path.expanduser("~/Desktop/photonbuilder"))
WM_PAGES = WM / "src" / "pages"
PB_PAGES = PB / "src" / "pages" / "sites" / "westmount"

# Track stats
stats = {
    "pages_copied": 0,
    "pages_skipped": 0,
    "pages_updated": 0,
    "data_files_copied": 0,
    "templates_copied": 0,
    "scripts_copied": 0,
    "static_iv_deleted": 0,
    "meta_standardized": 0,
    "errors": [],
}


def fix_import_path(content: str) -> str:
    """Fix layout import: ../layouts/ → ../../../layouts/ for PB nesting."""
    # Handle both quote styles
    content = content.replace(
        'from "../layouts/SiteLayout.astro"',
        'from "../../../layouts/SiteLayout.astro"'
    )
    content = content.replace(
        "from '../layouts/SiteLayout.astro'",
        'from "../../../layouts/SiteLayout.astro"'
    )
    # Fix template imports too
    content = content.replace(
        "from '../templates/IntrinsicValuePage.astro'",
        'from "../../../templates/IntrinsicValuePage.astro"'
    )
    content = content.replace(
        "from '../templates/ProspectScorePage.astro'",
        'from "../../../templates/ProspectScorePage.astro"'
    )
    # Fix data imports (../data/ → ../../../data/)
    content = re.sub(
        r"""(from\s+['"])\.\.\/data\/""",
        r'\1../../../data/',
        content
    )
    # Fix import.meta.glob paths for data
    content = re.sub(
        r"""(import\.meta\.glob\(['"])\.\.\/data\/""",
        r'\1../../../data/',
        content
    )
    return content


def standardize_meta(content: str) -> str:
    """Standardize section → category in export const meta."""
    # Only replace inside the meta block
    if "section:" in content and "export const meta" in content:
        content = re.sub(
            r"(\s+)section:\s*['\"](\w+)['\"]",
            r"\1category: '\2'",
            content
        )
        return content
    return content


def copy_unique_pages():
    """Copy pages that only exist in westmount repo → PB."""
    print("\n📄 Phase 1: Copying unique pages...")

    wm_pages = {f.name for f in WM_PAGES.glob("*.astro")}
    pb_pages = {f.name for f in PB_PAGES.glob("*.astro")}

    unique_to_wm = wm_pages - pb_pages
    common = wm_pages & pb_pages

    for page_name in sorted(unique_to_wm):
        src = WM_PAGES / page_name
        dst = PB_PAGES / page_name
        try:
            content = src.read_text()
            content = fix_import_path(content)
            content = standardize_meta(content)
            dst.write_text(content)
            stats["pages_copied"] += 1
            print(f"  ✅ {page_name}")
        except Exception as e:
            stats["errors"].append(f"Page {page_name}: {e}")
            print(f"  ❌ {page_name}: {e}")

    # For common pages, check if westmount version is newer (has more content or features)
    print(f"\n  📊 {len(unique_to_wm)} unique pages copied")
    print(f"  📊 {len(common)} pages exist in both (keeping PB versions)")
    print(f"  📊 {len(pb_pages - wm_pages)} pages only in PB (untouched)")


def copy_dynamic_routes():
    """Copy dynamic route files ([...ivslug].astro, [...prospectslug].astro)."""
    print("\n🔀 Phase 2: Copying dynamic routes...")

    for route_file in ["[...ivslug].astro", "[...prospectslug].astro"]:
        src = WM_PAGES / route_file
        dst = PB_PAGES / route_file
        if src.exists():
            content = src.read_text()
            content = fix_import_path(content)
            dst.write_text(content)
            stats["pages_copied"] += 1
            print(f"  ✅ {route_file}")
        else:
            print(f"  ⚠️  {route_file} not found in westmount")


def copy_templates():
    """Copy template components."""
    print("\n🧩 Phase 3: Copying templates...")

    src_dir = WM / "src" / "templates"
    dst_dir = PB / "src" / "templates"
    dst_dir.mkdir(parents=True, exist_ok=True)

    if src_dir.exists():
        for tmpl in src_dir.glob("*.astro"):
            content = tmpl.read_text()
            # Templates import from ../layouts/ which is correct for PB too
            # (templates/ is at same level as layouts/)
            (dst_dir / tmpl.name).write_text(content)
            stats["templates_copied"] += 1
            print(f"  ✅ {tmpl.name}")


def copy_types():
    """Copy TypeScript type definitions."""
    print("\n📝 Phase 4: Copying types...")

    src_dir = WM / "src" / "types"
    dst_dir = PB / "src" / "types"
    dst_dir.mkdir(parents=True, exist_ok=True)

    if src_dir.exists():
        for ts_file in src_dir.glob("*.ts"):
            shutil.copy2(ts_file, dst_dir / ts_file.name)
            print(f"  ✅ {ts_file.name}")


def copy_data_files():
    """Copy data files (IV JSONs, prospect JSONs, registry, cross-links, etc.)."""
    print("\n📊 Phase 5: Copying data files...")

    wm_data = WM / "src" / "data"
    pb_data = PB / "src" / "data"

    # Files/dirs unique to westmount that PB needs
    items_to_copy = [
        "iv",                       # ~500 IV JSON files
        "prospect",                 # ~1500 prospect JSON files
        "pages-registry.json",
        "cross-links.json",
        "dashboard-scores.json",
        "build-queue.json",
        "keyword-opportunities.json",
        "keyword-state.json",
    ]

    for item in items_to_copy:
        src = wm_data / item
        dst = pb_data / item

        if not src.exists():
            print(f"  ⚠️  {item} not found in westmount, skipping")
            continue

        if src.is_dir():
            # For directories, merge (don't overwrite existing)
            dst.mkdir(parents=True, exist_ok=True)
            count = 0
            for json_file in src.glob("*.json"):
                dst_file = dst / json_file.name
                if not dst_file.exists() or json_file.stat().st_mtime > dst_file.stat().st_mtime:
                    shutil.copy2(json_file, dst_file)
                    count += 1
            stats["data_files_copied"] += count
            print(f"  ✅ {item}/ ({count} files)")
        else:
            shutil.copy2(src, dst)
            stats["data_files_copied"] += 1
            print(f"  ✅ {item}")

    # Also update short-interest if westmount version is newer
    wm_si = wm_data / "short-interest"
    pb_si = pb_data / "short-interest"
    if wm_si.exists() and pb_si.exists():
        count = 0
        for f in wm_si.rglob("*.json"):
            rel = f.relative_to(wm_si)
            dst = pb_si / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists() or f.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(f, dst)
                count += 1
        if count:
            print(f"  ✅ short-interest/ ({count} files updated)")


def delete_static_iv_pages():
    """Delete static intrinsic-value pages that the dynamic route replaces."""
    print("\n🗑️  Phase 6: Removing static IV pages (replaced by dynamic route)...")

    # The dynamic route generates pages from src/data/iv/*.json
    # Find static pages that match the pattern *-intrinsic-value.astro
    iv_pattern = re.compile(r".*-intrinsic-value\.astro$")

    deleted = []
    for page in PB_PAGES.glob("*-intrinsic-value.astro"):
        page.unlink()
        deleted.append(page.name)
        stats["static_iv_deleted"] += 1

    if deleted:
        print(f"  🗑️  Deleted {len(deleted)} static IV pages")
        for d in deleted[:5]:
            print(f"      {d}")
        if len(deleted) > 5:
            print(f"      ... and {len(deleted) - 5} more")
    else:
        print("  ℹ️  No static IV pages found to delete")


def copy_scripts():
    """Copy westmount-specific scripts."""
    print("\n📜 Phase 7: Copying scripts...")

    src_dir = WM / "scripts"
    dst_dir = PB / "scripts" / "westmount"
    dst_dir.mkdir(parents=True, exist_ok=True)

    if src_dir.exists():
        for script in src_dir.glob("*.py"):
            shutil.copy2(script, dst_dir / script.name)
            stats["scripts_copied"] += 1
            print(f"  ✅ {script.name}")


def standardize_existing_pages():
    """Standardize meta fields in existing PB westmount pages."""
    print("\n🔧 Phase 8: Standardizing meta fields in existing pages...")

    count = 0
    for page in PB_PAGES.glob("*.astro"):
        content = page.read_text()
        new_content = standardize_meta(content)
        if new_content != content:
            page.write_text(new_content)
            count += 1
    stats["meta_standardized"] = count
    print(f"  ✅ {count} pages updated (section → category)")


def update_config_nav():
    """Update westmount nav in PB's sites.ts to match standalone repo."""
    print("\n⚙️  Phase 9: Updating westmount config...")

    config_path = PB / "src" / "config" / "sites.ts"
    content = config_path.read_text()

    # Update westmount nav to match the standalone repo's improved nav
    old_nav = """nav: [
      { label: 'Studies', href: '/#studies' },
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
    ]"""

    new_nav = """nav: [
      { label: 'Tools', href: '/#tools' },
      { label: 'Guides', href: '/#guides' },
      { label: 'Lists', href: '/#lists' },
      { label: 'IV Dashboard', href: '/intrinsic-value-dashboard/' },
    ]"""

    if old_nav in content:
        content = content.replace(old_nav, new_nav)
        config_path.write_text(content)
        print("  ✅ Nav updated (added IV Dashboard)")
    else:
        print("  ℹ️  Nav already updated or format differs")


def print_summary():
    """Print migration summary."""
    print("\n" + "=" * 60)
    print("📋 MIGRATION SUMMARY")
    print("=" * 60)
    print(f"  Pages copied:        {stats['pages_copied']}")
    print(f"  Templates copied:    {stats['templates_copied']}")
    print(f"  Data files copied:   {stats['data_files_copied']}")
    print(f"  Scripts copied:      {stats['scripts_copied']}")
    print(f"  Static IV deleted:   {stats['static_iv_deleted']}")
    print(f"  Meta standardized:   {stats['meta_standardized']}")

    if stats["errors"]:
        print(f"\n  ⚠️  {len(stats['errors'])} errors:")
        for err in stats["errors"]:
            print(f"      {err}")

    total_pages = len(list(PB_PAGES.glob("*.astro")))
    print(f"\n  Total westmount pages in PB: {total_pages}")
    print("\n  🔜 Next steps:")
    print("    1. Review layout merge (newsletter bar)")
    print("    2. Run: cd ~/Desktop/photonbuilder && npm run build")
    print("    3. Verify no build errors")
    print("    4. git add -A && git commit -m 'feat: migrate westmount back into monorepo'")
    print("    5. Update factory/cron configs")
    print("    6. Archive westmount-fundamentals repo")


if __name__ == "__main__":
    print("🚀 Westmount → PhotonBuilder Migration")
    print("=" * 60)

    # Verify both repos exist
    if not WM.exists():
        print("❌ westmount-fundamentals repo not found!")
        exit(1)
    if not PB.exists():
        print("❌ photonbuilder repo not found!")
        exit(1)

    copy_unique_pages()
    copy_dynamic_routes()
    copy_templates()
    copy_types()
    copy_data_files()
    delete_static_iv_pages()
    copy_scripts()
    standardize_existing_pages()
    update_config_nav()
    print_summary()
