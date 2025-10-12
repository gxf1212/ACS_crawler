#!/bin/bash

# LaTeX编译脚本 - 生成软件著作权申请材料PDF
# 适用于Ubuntu系统，使用XeLaTeX编译器
# 
# 使用方法：
#   chmod +x compile.sh
#   ./compile.sh

set -e  # 遇到错误立即退出

# 颜色输出定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    print_info "检查LaTeX编译环境..."
    
    if ! command -v xelatex &> /dev/null; then
        print_error "XeLaTeX未安装！请运行以下命令安装："
        echo "sudo apt update"
        echo "sudo apt install texlive-full"
        echo "或者安装精简版："
        echo "sudo apt install texlive-latex-base texlive-xetex texlive-lang-chinese texlive-fonts-recommended texlive-latex-extra texlive-science"
        exit 1
    fi
    
    if ! command -v bibtex &> /dev/null; then
        print_error "BibTeX未安装！请安装texlive-latex-extra包"
        exit 1
    fi
    
    print_success "LaTeX环境检查通过"
}

# 检查特定LaTeX包
check_latex_packages() {
    print_info "检查必需的LaTeX包..."
    
    # 创建临时测试文件来检查包
    local test_file="package_test.tex"
    cat > "$test_file" << 'EOF'
\documentclass{article}
\usepackage{newtxtext,newtxmath}
\usepackage{chemmacros}
\usepackage{tcolorbox}
\usepackage{fontspec}
\usepackage{xeCJK}
\begin{document}
Package test
\end{document}
EOF
    
    # 尝试编译测试文件
    if xelatex -interaction=batchmode "$test_file" > /dev/null 2>&1; then
        print_success "所需LaTeX包检查通过"
    else
        print_warning "某些LaTeX包可能缺失，建议安装完整版："
        echo "sudo apt install texlive-full"
        echo "或安装特定包："
        echo "sudo apt install texlive-fonts-extra texlive-science texlive-latex-extra"
        print_info "继续编译，如遇到包缺失错误请手动安装"
    fi
    
    # 清理测试文件
    rm -f package_test.* 2>/dev/null
}

# 清理临时文件
cleanup() {
    print_info "清理临时文件..."
    rm -f *.aux *.log *.toc *.out *.fdb_latexmk *.fls *.synctex.gz *.bbl *.blg *.idx *.ind *.ilg *.lof *.lot *.nav *.snm *.vrb *.xdv *.figlist *.makefile *.fls_latexmk *.run.xml *-blx.bib package_test.*
    print_success "临时文件清理完成"
}

# 编译单个LaTeX文件
compile_single() {
    local tex_file=$1
    local base_name=$(basename "$tex_file" .tex)
    
    print_info "编译 $tex_file..."
    
    # 第一次编译 - 生成辅助文件
    print_info "第一次XeLaTeX编译..."
    xelatex -synctex=1 -interaction=nonstopmode "$tex_file" || {
        print_error "第一次编译失败，请检查LaTeX语法错误"
        return 1
    }
    
    # 如果有.bib文件，运行BibTeX
    if [ -f "${base_name}.bib" ]; then
        print_info "运行BibTeX处理参考文献..."
        bibtex "${base_name}" || {
            print_warning "BibTeX处理失败，但继续编译"
        }
    fi
    
    # 第二次编译 - 处理交叉引用
    print_info "第二次XeLaTeX编译..."
    xelatex -synctex=1 -interaction=nonstopmode "$tex_file" || {
        print_error "第二次编译失败"
        return 1
    }
    
    # 第三次编译 - 确保所有引用正确
    print_info "第三次XeLaTeX编译..."
    xelatex -synctex=1 -interaction=nonstopmode "$tex_file" || {
        print_error "第三次编译失败"
        return 1
    }
    
    print_success "成功生成 ${base_name}.pdf"
}

# 主编译函数
main() {
    print_info "开始编译软件著作权申请材料..."
    
    # 检查当前目录
    if [ ! -f "document.tex" ]; then
        print_error "未找到document.tex文件！请确保在software-copyright目录下运行此脚本"
        exit 1
    fi
    
    # 检查依赖
    check_dependencies
    
    # 检查LaTeX包
    check_latex_packages
    
    # 检查中文字体支持
    print_info "检查中文字体支持..."
    if ! fc-list | grep -qi "noto.*cjk"; then
        print_warning "建议安装中文字体包以获得更好的显示效果："
        echo "sudo apt-get install fonts-noto-cjk"
        print_info "如果字体错误持续，请尝试安装："
        echo "sudo apt-get install fonts-liberation"
    fi
    
    # 清理旧的临时文件
    cleanup
    
    # 编译主文档
    compile_single "document.tex"
    
    # 最终清理
    cleanup
    
    # 检查输出文件
    if [ -f "document.pdf" ]; then
        print_success "编译完成！生成文件：document.pdf"
        print_info "PDF文件大小：$(du -h document.pdf | cut -f1)"
        
        # 可选：打开PDF文件
        if command -v evince &> /dev/null; then
            print_info "是否要打开PDF文件？(y/n)"
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                evince document.pdf &
            fi
        fi
    else
        print_error "编译失败，未生成PDF文件"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo "LaTeX编译脚本 - 软件著作权申请材料"
    echo ""
    echo "用法："
    echo "  ./compile.sh          - 编译生成PDF"
    echo "  ./compile.sh clean    - 清理临时文件"
    echo "  ./compile.sh help     - 显示此帮助信息"
    echo ""
    echo "环境要求："
    echo "  - Ubuntu系统"
    echo "  - 已安装XeLaTeX (texlive-xetex)"
    echo "  - 已安装中文字体支持 (texlive-lang-chinese)"
    echo ""
    echo "安装命令："
    echo "  sudo apt update"
    echo "  sudo apt install texlive-full"
    echo ""
    echo "或精简安装："
    echo "  sudo apt install texlive-latex-base texlive-xetex texlive-lang-chinese texlive-fonts-recommended"
}

# 解析命令行参数
case "${1:-}" in
    clean)
        cleanup
        exit 0
        ;;
    help|--help|-h)
        show_help
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_error "未知参数: $1"
        echo "使用 './compile.sh help' 查看帮助信息"
        exit 1
        ;;
esac