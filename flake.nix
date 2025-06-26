{
  description = "EnrichLayer Python API development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=master";

    flake-compat.url = "https://flakehub.com/f/edolstra/flake-compat/1";
    flake-utils.url = "https://flakehub.com/f/numtide/flake-utils/0.1";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          # Core HTTP dependencies
          aiohttp
          requests
          
          # Async frameworks
          gevent
          twisted
          treq
          
          # Testing dependencies
          pytest
          pytest-asyncio
          pytest-mock
          
          # Development tools
          black
          flake8
          mypy
          
          # Build tools
          setuptools
          wheel
          build
          
          # Additional utilities
          pyyaml
          click
        ]);
        
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            git
          ];
          
          shellHook = ''
            echo "🚀 EnrichLayer development environment loaded!"
            echo "Python version: $(python --version)"
            echo "Available packages:"
            echo "  - aiohttp (async HTTP client)"
            echo "  - gevent (green threads)"
            echo "  - twisted (async framework)"
            echo "  - pytest (testing)"
            echo "  - black, flake8, mypy (code quality)"
            echo ""
            echo "💡 Run tests with: python test_compatibility_dry_run.py"
            echo "💡 Install package in dev mode: pip install -e ."
          '';
        };
        
        # For CI/CD environments
        packages.default = pythonEnv;
      });
}
