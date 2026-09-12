{
  description = "nele devshell";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs =
    {
      nixpkgs,
      ...
    }:
    let
      systems = nixpkgs.lib.platforms.unix;
      eachSystem =
        f:
        nixpkgs.lib.genAttrs systems (
          system:
          f (
            import nixpkgs {
              inherit system;
              config = { };
              overlays = [ ];
            }
          )
        );
      deps =
        p: with p; [
          cmarkgfm
          python-frontmatter
          jinja2
          docopt
        ];
    in
    {
      devShells = eachSystem (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            (python3.withPackages (
              p:
              (deps p)
              ++ [
                p.flake8
                p.setuptools
              ]
            ))
          ];
        };
      });

      packages = eachSystem (
        pkgs:
        let
          fs = pkgs.lib.fileset;
          root = ./.;
          pypkgs = pkgs.python3Packages;
          nele = pypkgs.buildPythonPackage {
            pname = "nele";
            version = "0.5.0";
            src = fs.toSource {
              inherit root;
              fileset = fs.intersection (fs.gitTracked root) (
                fs.fileFilter (
                  f:
                  (f.hasExt "py")
                  || (f.name == "requirements.txt")
                  || (f.name == "setup.py")
                  || (f.name == "setup.cfg")
                ) root
              );
            };
            propagatedBuildInputs = deps pypkgs;
            pyproject = true;
            build-system = [ pypkgs.setuptools ];
          };
        in
        {
          inherit nele;
          default = nele;
        }
      );
    };
}
