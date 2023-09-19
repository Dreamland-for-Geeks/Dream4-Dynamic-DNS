import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

if __name__ == '__main__':
    import common_functions
    from update_ip_dns import main
    main()