import subprocess

# nên implement interface để có thể mở rộng sang dùng tool khác
class Terraform:
    def __init__(self, path_to_tf_workspace: str):
        self.path_to_tf_workspace = path_to_tf_workspace

    def refresh(self):
        try:
            result = subprocess.run(
                ["terraform", "apply", "-refresh-only", "-auto-approve"],
                cwd=self.path_to_tf_workspace,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"tf refresh failed: {e.returncode} {e.stderr}")
        except Exception as e:
            raise Exception(f"{e}")
        
    def show_json(self):
        try:
            result = subprocess.run(
                ["terraform", "show", "-json"],
                cwd=self.path_to_tf_workspace,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"tf show json failed: {e.returncode} {e.stderr}")
        except Exception as e:
            raise Exception(f"{e}")
        
    def graph(self):
        try:
            result = subprocess.run(
                ["terraform", "graph"],
                cwd=self.path_to_tf_workspace,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"tf graph failed: {e.returncode} {e.stderr}")
        except Exception as e:
            raise Exception(f"{e}")
        
    def init(self):
        try:
            result = subprocess.run(
                ["terraform", "init"],
                cwd=self.path_to_tf_workspace,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"tf init failed: {e.returncode} {e.stderr}")
        except Exception as e:
            raise Exception(f"{e}")
        
    def apply(self):
        try:
            result = subprocess.run(
                ["terraform", "apply", "-auto-approve"],
                cwd=self.path_to_tf_workspace,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"tf apply failed: {e.returncode} {e.stderr}")
        except Exception as e:
            raise Exception(f"{e}")
        
    def destroy(self):
        try:
            result = subprocess.run(
                ["terraform", "destroy", "-auto-approve"],
                cwd=self.path_to_tf_workspace,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"tf destroy failed: {e.returncode} {e.stderr}")
        except Exception as e:
            raise Exception(f"{e}")