import os
import tempfile
import base64
from analyzer.analyzer import analyze_directory, get_file_info
from analyzer.permissions import get_permission_risks, report_unusual_permissions
from analyzer.file_types import categorize_file

# Valid base64 for a minimal JPEG file (1x1 pixel)
MINIMAL_JPEG_BASE64 = (
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAUDBBQEBQUGBQUHBwYIBwcICQsJCAgKCAcHCgsKCQkK"
    "DAwMCAsLDAwKCgsMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/2wBDAQcHBwoICAkICQwMDAwMDAwM"
    "DAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEB"
    "AxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAdEAABBQADAQAAAAAAAAAAAAABAAIDBAUGBx"
    "Eh/8QAFQEBAQAAAAAAAAAAAAAAAAAAAgP/xAAWEQEBAQAAAAAAAAAAAAAAAAABAgP/2gAMAwEA"
    "AhEDEQA/AMvERAREQEREBERAREQEREBERAX//2Q=="
)

# Valid base64 for a minimal MP4 container (1-second blank, no video track)
MINIMAL_MP4_BASE64 = (
    "AAAAHGZ0eXBNNAACAAACAAABAQAAAAEAAAKkbW9vdgAAAGxtdmhkAAAAANr/AAAC3QAAADYAAAB9"
    "AAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAB"
    "AAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAEA"
    "AAAAAAAAAAAAAAAAAAAAAAgAAABsbXZoZAAAAADa/wAAA90AAAAPAAABAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
)


def write_minimal_jpeg(path):
    with open(path, "wb") as f:
        f.write(base64.b64decode(MINIMAL_JPEG_BASE64))


def write_minimal_mp4(path):
    with open(path, "wb") as f:
        f.write(base64.b64decode(MINIMAL_MP4_BASE64))


def test_basic_functionality():
    """Test basic file analysis works."""
    # Create a temp directory with some files
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create test files
        test_file = os.path.join(tmp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("hello world")

        # Test get_file_info
        info = get_file_info(test_file)
        assert "error" not in info
        assert info["size"] > 0
        assert info["extension"] == ".txt"
        assert info["category"] == "Text"

        # Test analyze_directory
        results = analyze_directory(tmp_dir)
        assert len(results) == 1
        assert results[0]["path"] == test_file


def test_file_categorization():
    """Test file type detection."""
    test_cases = [
        ("test.txt", "Text"),
        ("image.jpg", "Image"),
        ("video.mp4", "Video"),
        ("unknown.xyz", "Text"),
    ]

    with tempfile.TemporaryDirectory() as tmp_dir:
        for filename, expected_category in test_cases:
            filepath = os.path.join(tmp_dir, filename)

            if filename.endswith(".jpg"):
                write_minimal_jpeg(filepath)
            elif filename.endswith(".mp4"):
                write_minimal_mp4(filepath)
            else:
                with open(filepath, "w") as f:
                    f.write("test")

            category = categorize_file(filepath)
            print(f"{filename} -> {category} (expected: {expected_category})")
            assert category == expected_category


def test_permission_risks():
    """Test permission risk detection."""
    # Test world-writable
    risks = get_permission_risks(0o666)  # rw-rw-rw-
    assert "World-writable" in risks

    # Test setuid
    risks = get_permission_risks(0o4755)  # rwsr-xr-x
    assert "Setuid bit set" in risks

    # Test normal permissions
    risks = get_permission_risks(0o644)  # rw-r--r--
    assert len(risks) == 0


def test_error_handling():
    """Test error handling for inaccessible files."""
    # Test non-existent file
    info = get_file_info("/nonexistent/file.txt")
    assert "error" in info

    # Test non-existent directory
    results = analyze_directory("/nonexistent/directory")
    # Should return empty list, not crash
    assert len(results) == 0


def test_large_file_detection():
    """Test large file identification."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a large file (5MB)
        large_file = os.path.join(tmp_dir, "large.bin")
        with open(large_file, "wb") as f:
            f.write(b"x" * (5 * 1024 * 1024))

        results = analyze_directory(tmp_dir)
        assert len(results) == 1
        assert results[0]["size"] == 5 * 1024 * 1024


def test_permissions_report():
    """Test unusual permissions reporting."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create file with risky permissions
        risky_file = os.path.join(tmp_dir, "risky.txt")
        with open(risky_file, "w") as f:
            f.write("dangerous")
        os.chmod(risky_file, 0o666)  # World-writable

        results = analyze_directory(tmp_dir)
        risky_files = report_unusual_permissions(results)

        assert len(risky_files) == 1
        assert "World-writable" in risky_files[0]["risk_reasons"]


# Run a quick integration test
def integration_test():
    """Test the whole thing works together."""
    print("\n" + "=" * 50)
    print("INTEGRATION TEST")
    print("=" * 50)

    # Test on a real directory (current directory)
    current_dir = "."
    print(f"Testing on: {os.path.abspath(current_dir)}")

    try:
        results = analyze_directory(current_dir)
        print(f"Found {len(results)} files")

        # Show some stats
        categories = {}
        for file_info in results:
            if "error" not in file_info:
                cat = file_info["category"]
                categories[cat] = categories.get(cat, 0) + 1

        print("\nFile categories found:")
        for cat, count in categories.items():
            print(f"  {cat}: {count}")

        # Check for risky files
        risky_files = report_unusual_permissions(results)
        print(f"\nFiles with unusual permissions: {len(risky_files)}")

    except Exception as e:
        print(f"Integration test failed: {e}")


if __name__ == "__main__":
    print("Running basic tests...")

    try:
        test_basic_functionality()
        print("✓ Basic functionality test passed")

        test_file_categorization()
        print("✓ File categorization test passed")

        test_permission_risks()
        print("✓ Permission risks test passed")

        test_error_handling()
        print("✓ Error handling test passed")

        test_large_file_detection()
        print("✓ Large file detection test passed")

        test_permissions_report()
        print("✓ Permissions report test passed")

        print("\nAll tests passed! 🎉")

        integration_test()

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
